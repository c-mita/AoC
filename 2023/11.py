import itertools


def parse_file(filename):
    space = set()
    with open(filename) as f:
        for r, line in enumerate(f):
            for c, s in enumerate(line.strip()):
                if s == "#":
                    space.add((r, c))
    return space


def expand_space(space, shift_amount=1):
    rows = max(s[0] for s in space) + 1
    cols = max(s[1] for s in space) + 1
    expanded_rows = {}
    to_shift = 0
    for r in range(rows):
        points = [c for c in range(cols) if (r, c) in space]
        if not points:
            to_shift += shift_amount
        for c in points:
            expanded_rows[(r, c)] = (r+to_shift, c)

    to_shift = 0
    expanded_cols = {}
    for c in range(cols):
        points = [r for r in range(rows) if (r, c) in space]
        if not points:
            to_shift += shift_amount
        for r in points:
            expanded_cols[(r, c)] = (r, c+to_shift)

    expanded = set()
    for (r, c) in space:
        expanded.add((expanded_rows[(r, c)][0], expanded_cols[(r, c)][1]))
    return expanded


def calc_distances(space):
    for l, r in itertools.combinations(space, 2):
        l0, l1 = l
        r0, r1 = r
        yield abs(r0-l0) + abs(r1-l1)


space = parse_file("11.txt")
expanded = expand_space(space)
distance_sums = sum(calc_distances(expanded))
print(distance_sums)

super_expanded = expand_space(space, shift_amount=999999)
super_distance_sums = sum(calc_distances(super_expanded))
print(super_distance_sums)
