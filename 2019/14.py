import math
import re
from collections import Counter, namedtuple

ReactionInput = namedtuple("ReactionInput", ["name", "quantity"])

testing = {"FUEL":(1, [ReactionInput("A", 7), ReactionInput("E", 1)]),
    "E":(1, [ReactionInput("A", 7), ReactionInput("D", 1)]),
    "D":(1, [ReactionInput("A", 7), ReactionInput("C", 1)]),
    "C":(1, [ReactionInput("A", 7), ReactionInput("B", 1)]),
    "B":(1, [ReactionInput("ORE", 1)]),
    "A":(10, [ReactionInput("ORE", 10)])}

testing_2 = {"FUEL":(1, [ReactionInput("CA", 4), ReactionInput("BC", 3), ReactionInput("AB", 2)]),
    "CA":(1, [ReactionInput("A", 1), ReactionInput("C", 4)]),
    "BC":(1, [ReactionInput("B", 5), ReactionInput("C", 7)]),
    "AB":(1, [ReactionInput("B", 4), ReactionInput("A",3)]),
    "C":(5, [ReactionInput("ORE", 7)]),
    "B":(3, [ReactionInput("ORE", 8)]),
    "A":(2, [ReactionInput("ORE", 9)]),}


def parse_reaction(line):
    inputs, outputs = line.split(" => ")
    quantity, output = outputs.split(" ")
    output = output.strip()
    quantity = int(quantity)

    inputs = [tuple(x.split(" ")) for x in inputs.split(", ")]
    inputs = [ReactionInput(r.strip(), int(q)) for (q, r) in inputs]
    return output, quantity, inputs


def parse_input(filename):
    reactions = {}
    with open(filename) as f:
        for line in f:
            output, quantity, inputs = parse_reaction(line)
            reactions[output] = (quantity, inputs)
    return reactions


def calc_ore(require, reactions):
    # BFS/DFS (doesn't really matter which) to calculate ore requirements for given input
    # tracks unused outputs to reuse results from previous reactions
    inventory = Counter()
    ore_needed = 0
    while require:
        target, quantity = require.pop() #pop(0) to make BFS
        quantity -= inventory[target]
        if quantity <= 0:
            inventory[target] = -quantity
            continue
        else:
            inventory[target] = 0
        produced, reaction = reactions[target]
        scale = int(math.ceil(float(quantity) / produced))
        for (reagent, amount) in reaction:
            amount *= scale
            if reagent == 'ORE':
                ore_needed += amount
                continue
            require.append((reagent, amount))

        remaining = produced * scale - quantity
        assert remaining >= 0
        inventory[target] += remaining
    return ore_needed


# Part 1 - simply calculate ore needed for a single fuel input
reactions = parse_input("14_input.txt")
require = [("FUEL", 1)]
ore_required = calc_ore(require, reactions)
print ore_required


# Part 2 - exponentially grow fuel demand to exceed allowed ore input
# then binary search over input to find maximum
def binary_search(lower, upper, func):
    if not func(lower) or func(upper):
        raise ValueError("function not consistent with provided range")
    while True:
        if upper - lower <= 4:
            for n in xrange(lower, upper+1):
                if not func(n):
                    return n - 1
        q = (upper + lower) / 2
        v = func(q)
        if v:
            lower = q
        else:
            upper = q

demand = 1
while calc_ore([('FUEL', demand)], reactions) < 1e12:
    demand *= 2

func = lambda v: calc_ore([('FUEL', v)], reactions) < 1e12
maximum_fuel = binary_search(demand / 2, demand, func)
print maximum_fuel
