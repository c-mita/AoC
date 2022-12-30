import math

"""
Part 1 is straightforward; just build the AST and evaluate it.

For part 2, evaluate the tree as much as possible and descend
down the branch with unknown values, at each step calculating
what the value should be.
A little care is needed because "-" and "/" are not commutative.
"""


def parse_file(filename):
    monkeys = {}
    with open(filename) as f:
        for line in f:
            target, op = line.strip().split(": ")
            things = op.split(" ")
            if len(things) > 1:
                monkeys[target] = (things[0], things[1], things[2])
            else:
                monkeys[target] = int(op)
    return monkeys


def evaluate(target, monkeys):
    updated_monkeys = {}
    def rec(monkey):
        if monkey in updated_monkeys:
            # if our input is a tree then this branch is never hit
            return updated_monkeys[monkey]
        thing = monkeys[monkey]
        if type(thing) == int or type(thing) == float:
            updated_monkeys[monkey] = thing
            return thing
        l, op, r = thing
        vl = rec(l)
        vr = rec(r)
        if op == "+":
            v = vl + vr
        elif op == "-":
            v = vl - vr
        elif op == "/":
            v = vl / vr
        elif op == "*":
            v = vl * vr
        else:
            raise ValueError("Unknown op '%s'" % op)
        updated_monkeys[monkey] = v
        return v
    return rec(target), updated_monkeys


def find_unknown(monkeys):
    # assumes our input is a tree, or at least that there is exaxtly
    # one path between the root and the leaf with the unknown value
    _, evaluated = evaluate("root", monkeys)
    def search(target, value):
        children = monkeys[target]
        if not type(children) == tuple:
            if not math.isnan(children):
                raise ValueError("Oops?")
            return value
        left, op, right = children
        need_right = math.isnan(evaluated[right])
        known = left if need_right else right
        unknown = right if need_right else left
        kv = evaluated[known]
        if op == "+":
            nv = value - kv
        elif op == "-":
            # value = known - unknown OR value = unknown -known
            # unknwon = value - known OR unknown = value + known
            nv = kv - value if need_right else value + kv
        elif op == "*":
            nv = value / kv
        elif op == "/":
            # value = known / unknown OR value = unknown / known
            # unkown = known / value OR unknown = value * known
            nv = kv / value if need_right else kv * value
        else:
            raise ValueError("Unknown op '%s'" % op)
        return search(unknown, nv)
    left, op, right = monkeys["root"]
    if math.isnan(evaluated[left]):
        return search(left, evaluated[right])
    else:
        return search(right, evaluated[left])



monkeys = parse_file("21_input.txt")
root, evaluated_monkeys = evaluate("root", monkeys)
root = int(root)
print(root)

updated_monkeys = dict(monkeys)
updated_monkeys["humn"] = float("nan")
value = find_unknown(updated_monkeys)
value = int(value)
print(value)
