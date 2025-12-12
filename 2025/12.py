"""
So this appears to be very difficult on the surface.
And it is a large search space.

We assume that a cell can only be the "top-left" corner of a single
"present". This is valid if all presents occupy at least 5 cells of
their 3x3 box (they all do).

Then for each cell in the NxM grid, we try to place all orientations
of some present and recurse. So long as we traverse points in order,
we can assume a cell that didn't have the top-left corner of a present
placed there will never be considered again and can be removed from
consideration. This required the set of points is ordered but stil
has efficient lookup (i.e. a Python3 dict - sets aren't ordered).

Highly symmetric presents require fewer checks.

We terminate when we don't have enough space left to place all the
presents remaining.

It turns out this last check is sufficient to solve the problem input
but not the example input. Which is... weird, and non obvious.

Runtime ~40 seconds.
"""


import re


def parse_input(data):
    if type(data) == str:
        data = data.split("\n")

    def parse_block(stream):
        block = set()
        r = 0
        while line := next(stream).strip():
            for c, s in enumerate(line):
                if s == "#":
                    block.add((r, c))
            r += 1
        return block

    blocks = []
    spaces = []
    stream = iter(data)
    for line in stream:
        line = line.strip()
        if not line:
            continue
        if "x" in line:
            values = list(map(int, re.findall("[0-9]+", line)))
            spaces.append((tuple(values[:2]), tuple(values[2:])))
        else:
            blocks.append(parse_block(stream))
    return blocks, spaces


def mirror(shape):
    mirrored = set()
    flipped = set()
    for (r, c) in shape:
        mirrored.add((r, 2-c))
        flipped.add((2-r, c))
    yield tuple(sorted(mirrored))
    yield tuple(sorted(flipped))


def rotate(shape):
    for n in range(4):
        rotated = set()
        for (r, c) in shape:
            rotated.add((2-c, r))
        yield tuple(sorted(rotated))
        shape = rotated


def variants(shape):
    min_r = min(shape, key=lambda v:v[0])[0]
    min_c = min(shape, key=lambda v:v[1])[1]
    max_r = max(shape, key=lambda v:v[0])[0]
    max_c = max(shape, key=lambda v:v[1])[1]
    if not (min_c == min_r == 0) or not (max_c == max_r == 2):
        raise ValueError("Shape does not use 3x3 grid")
    if not len(shape) >= 5:
        raise ValueError("Solution only valid for presents of 5 cells or more")

    for rotation in rotate(shape):
        yield rotation
        yield from mirror(rotation)


def try_place(coord, space, shape):
    modified = dict(space)
    cx, cy = coord
    for px, py in shape:
        m = px + cx, py + cy
        if m not in modified:
            return None
        del modified[m]
    return modified


def can_pack(space, to_pack, presents):
    if all(t == 0 for t in to_pack):
        return True
    available = len(space)
    required = sum(len(presents[i][0]) * v for (i, v) in enumerate(to_pack))
    if required > available:
        return False

    new_pack = list(to_pack)
    subspace = dict(space)
    for point in space:
        if required > len(subspace):
            return False
        for shape_idx, amount in enumerate(to_pack):
            if not amount:
                continue
            for shape in presents[shape_idx]:
                if (modified := try_place(point, subspace, shape)) != None:
                    new_pack[shape_idx] -= 1
                    result = can_pack(modified, new_pack, presents)
                    if result:
                        return True
                    new_pack[shape_idx] += 1
        # this is valid if subspace is "ordered" - we depend on ordered dicts
        del subspace[point]
    return False


TEST_INPUT = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""


test_blocks, test_spaces = parse_input(TEST_INPUT)

with open("12.txt") as f:
    blocks, spaces = parse_input(f.readlines())
#blocks, spaces = test_blocks, test_spaces

shapes = []
for block in blocks:
    shapes.append(list(set(variants(block))))

total_possible = 0
for bounds, to_pack in spaces:
    world = {(r, c):True for r in range(bounds[0]) for c in range(bounds[1])}
    possible = can_pack(world, to_pack, shapes)
    print(bounds, to_pack, possible)
    if possible:
        total_possible += 1
print(total_possible)
