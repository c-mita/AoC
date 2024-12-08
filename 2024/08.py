"""
The problem statement is a little misleading and confusing.
The important part is that the problem statement gives that any two pairs
of antennas always give exactly two antinodes (unless outside the bounds).

So the problem seems to be explictly discarding the possibility of antinodes
between the two antennas, even if they fulfill the "one is twice as far away
as the other" requirement. This has implications simplifying part 2 (at least
for my input)
"""

import collections
import itertools

def parse_file(filename):
    space = {}
    with open(filename) as f:
        for r, line in enumerate(f):
            for c, s in enumerate(line.strip()):
                space[(r, c)] = "" if s == "." else s
    return space

def map_antennae(space):
    antennae = collections.defaultdict(list)
    for coord, item in space.items():
        if not item:
            continue
        antennae[item].append(coord)
    return antennae


def find_antinodes(antennae, space):
    nodes = set()
    for t in antennae:
        for n1, n2 in itertools.combinations(antennae[t], 2):
            dx = n2[1] - n1[1]
            dy = n2[0] - n1[0]
            a1 = n1[0] - dy, n1[1] - dx
            a2 = n2[0] + dy, n2[1] + dx
            if a1 in space:
                nodes.add(a1)
            if a2 in space:
                nodes.add(a2)
    return nodes


def find_repeated_antinodes(antennae, space):
    nodes = set()
    for t in antennae:
        for n1, n2 in itertools.combinations(antennae[t], 2):
            dx = n2[1] - n1[1]
            dy = n2[0] - n1[0]
            a1 = n1
            a2 = n2
            while a1 in space:
                nodes.add(a1)
                a1 = a1[0] - dy, a1[1] - dx
            while a2 in space:
                nodes.add(a2)
                a2 = a2[0] + dy, a2[1] + dx
    return nodes


space = parse_file("08.txt")
antennae = map_antennae(space)

antinodes = find_antinodes(antennae, space)
print(len(antinodes))

antinodes = find_repeated_antinodes(antennae, space)
print(len(antinodes))
