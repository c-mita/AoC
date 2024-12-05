import re
import itertools


def parse_file(filename):
    with open(filename) as f:
        return [l.strip() for l in f]


data = parse_file("03.txt")

s = 0
for l in data:
    for mul in re.findall("mul\([0-9]+,[0-9]+\)", l):
        l, r = map(int, re.findall("[0-9]+", mul))
        s += l * r
print(s)

relevant = itertools.chain.from_iterable(
        re.findall(
            "mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\)", d) for d in data
)
match = True
s = 0
for item in relevant:
    if item == "do()":
        match = True
    elif item == "don't()":
        match = False
    elif match:
        l, r = map(int, re.findall("[0-9]+", item))
        s += l * r
print(s)
