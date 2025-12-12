"""
A total rework of my original approach.

For Part 1 we just test every element of the powerset of switches.
There aren't many, this is fast. And we'll need the powerset anyway.

For Part 2, we no longer do a DFS search for individual button presses.
Compared to my previous approaches, I think this is beautiful. I wish I
could say I discovered it myself, but I encountered the basic idea first
on reddit.

Consider a joltage target (j1, j2, ..., jn).
Compute the parity of each element (p1, p2, .., pn) where (pi == ji % 2).
This is analagous to the "lights" in Part 1.

For each combination of buttons "C" that lead to this parity:
    * Apply the button presses to the target to get a new one.
    * The elements of the new target will all be even. We can safely
      divide every element by 2.
    * Recurse:
       S = recurse(new_target) * 2 + len(combination)
Return the minimal S from the loop

The recursive function can (and should) be memoized.
We can also precompute the mapping of parities to combinations.

Runtime ~0.6 seconds.
An improvement of a factor of 36,000 compared to my original 6 hour
solution.
"""


import collections
import itertools
import re


def parse_data(data):
    if type(data) == str:
        data = data.split("\n")
    for line in data:
        line = line.strip()
        if not line:
            continue
        target_pattern = re.findall(r"\[.*\]", line)[0][1:-1]
        switch_strings = re.findall(r"\(.*?\)", line)
        switches = []
        for switch in switch_strings:
            switches.append(tuple(map(int, re.findall("[0-9]+", switch))))
        joltages = re.findall("{.*}", line)[0]
        joltages = tuple(map(int, re.findall("[0-9]+", joltages)))
        yield target_pattern, switches, joltages


def powerset(elements):
    return itertools.chain.from_iterable(
            itertools.combinations(elements, r) for r in range(len(elements) + 1)
    )


def valid_combination(target, switch_set):
    value = 0
    for switch in switch_set:
        for s in switch:
            value ^= 1 << s
    return target == value


def valid_combinations(target, switches):
    i = 0
    target_value = 0
    for t in reversed(target):
        target_value <<= 1
        target_value |= 1 if t == "#" else 0
    for combination in powerset(switches):
        if valid_combination(target_value, combination):
            yield combination


def solve_joltages(target, switches):
    cache = {}
    parity_lookup = collections.defaultdict(list)

    for combination in powerset(switches):
        parity = [0] * len(target)
        for switch in combination:
            for s in switch:
                parity[s] ^= 1
        parity = tuple(parity)
        parity_lookup[parity].append(combination)

    def solve(target):
        if all(t == 0 for t in target):
            return 0
        if target in cache:
            return cache[target]
        parity = tuple(t % 2 for t in target)
        best = 0x7FFFFFFF
        if parity not in parity_lookup:
            return best
        for combination in parity_lookup[parity]:
            new_target = list(target)
            for switch in combination:
                for c in switch:
                    new_target[c] -= 1
            if any(t < 0 for t in new_target):
                continue
            # every target element is now even, so we can halve
            # it and just multiply the result of searching by two
            new_target = tuple(t // 2 for t in new_target)
            # we pressed len(combination) buttons to reach here
            solution = solve(new_target) * 2 + len(combination)
            best = min(best, solution)
        cache[target] = best
        return best
    return solve(target)


TEST_DATA = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""

test_entries = list(parse_data(TEST_DATA))
with open("10.txt") as f:
    entries = list(parse_data(f))

#entries = test_entries
s = 0
for target, switches, joltages in entries:
    s += min(len(combination) for combination in valid_combinations(target, switches))
print(s)


s = 0
for target, switches, joltages in entries:
    s += solve_joltages(joltages, switches)
print(s)
