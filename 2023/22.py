"""
The most useful way to view the bricks is as a graph of what supports what.
Settling is easy; just run through the bricks in order of height, maintain
a height bitmap (the x-y coordinates are tightly bounded), and shift z coords
down to avoid gaps. We can build the graph as we do this.

For part 2, we just walk the graph, tracking what will fall as we go.
We don't need a visited set when we do this because we might need to
revisit nodes again (after more have been identified as falling).
"""


import collections
import itertools


def parse_file(filename):
    bricks = []
    with open(filename) as f:
        for line in f:
            start, end = line.strip().split("~")
            start = tuple(map(int, start.split(",")))
            end = tuple(map(int, end.split(",")))
            bricks.append((start, end))
    return bricks


def settle_bricks(bricks):
    settled_bricks = []
    graph = {}
    bricks = sorted(bricks, key=lambda b: b[0][-1])
    heightmap = collections.defaultdict(lambda: (0, -1))

    for idx, brick in enumerate(bricks):
        sx, sy, sz = brick[0]
        ex, ey, ez = brick[1]
        rx = range(sx, ex+1)
        ry = range(sy, ey+1)
        mz = 0
        for x, y in itertools.product(rx, ry):
            z, _ = heightmap[(x, y)]
            if sz <= z:
                raise ValueError("Intersection?")
            if z > mz:
                mz = z

        to_fall = 0
        if sz > mz + 1:
            to_fall = sz - (mz + 1)
        sz, ez = sz - to_fall, ez - to_fall
        supports = set()
        for x, y in itertools.product(rx, ry):
            if heightmap[(x, y)][0] == sz - 1:
                supports.add(heightmap[(x, y)][1])
            heightmap[(x, y)] = ez, idx
        graph[idx] = list(supports)
        settled_bricks.append(((sx, sy, sz), (ex, ey, ez)))

    return settled_bricks, graph


def find_falls(graph, reverse_graph, target):
    removed = {target}
    falls = []
    to_visit = list(reverse_graph[target])
    to_visit = set(reverse_graph[target])
    while to_visit:
        brick = to_visit.pop()
        supported_by = [s for s in graph[brick] if s not in removed]
        if supported_by:
            continue
        falls.append(brick)
        removed.add(brick)
        for supporting in reverse_graph[brick]:
            to_visit.add(supporting)
    return falls


bricks = parse_file("22.txt")

settled, graph = settle_bricks(bricks)
reverse_graph = collections.defaultdict(list)
must_stay = set()
for brick, supports in graph.items():
    for s in supports:
        reverse_graph[s].append(brick)
    if len(supports) == 1:
        must_stay.add(supports[0])

safe_to_remove = [b for b in graph if b not in must_stay]
print(len(safe_to_remove))

already_fallen = set()
total_falls = sum(len(find_falls(graph, reverse_graph, brick)) for brick in graph)
print(total_falls)
