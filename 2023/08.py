"""
I don't like this...

Part 1 is fine. Just walk the graph following the instructions given until you get to
the target point.

Part 2 is... difficult. The problem is, is that we don't know, in general, what the
loops look like. The instructions could lead the different paths to intermingle, etc.

Except none of that is true! The input is constructed in such a way that there is a
distinct loop for each "starting" point _and_ that the lead time (before we first
see the target Z value) is exactly equal to the loop length!
So we just count how long before we see the target value for each point and then
compute the Lowest-Common-Multiple of those values.

Simultaneously a relief and a disappointment.
On the other hand, it is only Day 8.
"""


import re
import functools


def parse_input(filename):
    with open(filename) as f:
        lines = "".join(l for l in f)
    instructions, mapping = lines.split("\n\n")
    graph = {}
    for line in mapping.split("\n"):
        line = line.strip()
        if not line:
            continue
        source, left, right = re.findall("[A-Z]+", line)
        graph[source] = (left, right)
    return instructions, graph


def steps_to_target(instructions, mapping, start, target_func):
    def next_instruction():
        while True:
            for i in instructions:
                yield i
    n = 0
    current = start
    step_gen = next_instruction()
    while not target_func(current):
        lr = next(step_gen)
        current = mapping[current][0] if lr == "L" else mapping[current][1]
        n += 1
    return n


def gcd(a, b):
    if a < b:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a % b)


def lcm(a, b):
    return int(a * b / gcd(a, b))


instructions, mapping = parse_input("08.txt")
steps = steps_to_target(instructions, mapping, "AAA", lambda n: n == "ZZZ")
print(steps)

starts = {node for node in mapping if node[-1] == "A"}
targets = {node for node in mapping if node[-1] == "Z"}
assert len(starts) == len(targets)

target_func = lambda n: n[-1] == "Z"
steps = []
for start in starts:
    steps.append(steps_to_target(instructions, mapping, start, target_func))
print(steps)
result = functools.reduce(lcm, steps)
print(result)
