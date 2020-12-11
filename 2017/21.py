"""
12 31 43 24
34 42 21 13

21 34 13 42
43 12 24 31
"""

"""
123 741 987 369
456 852 654 258
789 963 321 147

321 789 147 963
654 456 258 852
987 123 369 741
"""


def generate_2x2_matches(pattern):
    rot_map = {1:3, 2:1, 3:4, 4:2}
    vert_map = {1:2, 2:1, 3:4, 4:3}
    horiz_map = {1:3, 2:4, 3:1, 4:2}
    d1_map = {1:1, 2:3, 3:2, 4:4}
    d2_map = {1:4, 2:2, 3:3, 4:1}
    rt = lambda v: rot_map[v]
    ht = lambda v: horiz_map[v]
    vt = lambda v: vert_map[v]
    d1t = lambda v: d1_map[v]
    d2t = lambda v: d2_map[v]
    patterns = [tuple(sorted(map(ht, pattern))), tuple(sorted(map(vt, pattern))),
            tuple(sorted(map(d1t, pattern))), tuple(sorted(map(d2t, pattern)))]
    rp = pattern
    for n in range(3):
        rp = tuple(sorted(map(rt, rp)))
        patterns.append(rp)
    return patterns


def generate_3x3_matches(pattern):
    rot_map = {1:7, 2:4, 3:1, 4:8, 5:5, 6:2, 7:9, 8:6, 9:3}
    vert_map = {1:3, 2:2, 3:1, 4:6, 5:5, 6:4, 7:9, 8:8, 9:7}
    horiz_map = {1:7, 2:8, 3:9, 4:4, 5:5, 6:6, 7:1, 8:2, 9:3}
    d1_map = {1:1, 2:4, 3:7, 4:2, 5:5, 6:8, 7:3, 8:6, 9:9}
    d2_map = {1:9, 2:6, 3:3, 4:8, 5:5, 6:2, 7:7, 8:4, 9:1}
    rt = lambda v: rot_map[v]
    ht = lambda v: horiz_map[v]
    vt = lambda v: vert_map[v]
    d1t = lambda v: d1_map[v]
    d2t = lambda v: d2_map[v]
    patterns = [tuple(sorted(map(ht, pattern))), tuple(sorted(map(vt, pattern))),
            tuple(sorted(map(d1t, pattern))), tuple(sorted(map(d2t, pattern)))]
    rp = pattern
    for n in range(3):
        rp = tuple(sorted(map(rt, rp)))
        patterns.append(rp)
    return patterns


def parse_pattern(pattern):
    rows = pattern.split("/")
    s = len(rows)
    return (s, tuple(n+1 for n, c in enumerate("".join(rows)) if c == "#"))


def parse_file(filename):
    mapping = {}
    with open(filename) as f:
        for l in f:
            in_pattern, out_pattern = l.strip().split(" => ")
            mapping[parse_pattern(in_pattern)] = parse_pattern(out_pattern)
    return mapping


def complete_mappings(mappings):
    completed = dict(mappings)
    for (s, i), o in mappings.items():
        if s == 2:
            for m in generate_2x2_matches(i):
                completed[(s, m)] = o
        elif s == 3:
            for m in generate_3x3_matches(i):
                completed[(s, m)] = o
        else:
            raise ValueError("Bad Size!")

    return completed


def decompose_grid(grid):
    l = int(len(grid)**0.5)
    sl = 2 if l % 2 == 0 else 3
    subgrids = []
    for r in range(l / sl):
        grid_row = grid[r*l*sl: r*l*sl + l*sl]
        subgrid_row = []
        for c in range(l / sl):
            subgrid = sum((grid_row[l*n + c*sl : l*n + c*sl + sl] for n in range(sl)), [])
            subgrid_row.append(subgrid)
        subgrids.append(subgrid_row)
    return subgrids


def rebuild_grid(subgrids):
    rows = len(subgrids)
    columns = len(subgrids[0])
    gsize = len(subgrids[0][0])
    grid = [0] * rows * columns * gsize
    l = int(len(grid) ** 0.5)
    sl = int(gsize ** 0.5)
    for rn, row_grids in enumerate(subgrids):
        for cn, subgrid in enumerate(row_grids):
            for n in range(sl):
                grid[l*sl*rn + sl*cn + l*n : l*sl*rn + sl*cn + l*n + sl] = subgrid[n*sl : n*sl + sl]
    return grid


def cycle(grid, rules):
    subgrids = decompose_grid(grid)
    new_grids = []
    for row in subgrids:
        new_row = []
        for g in row:
            s = 2 if len(g) == 4 else 3
            key = (s, tuple(n+1 for n, v in enumerate(g) if v))
            new_key = rules[key]
            new_grid = list(range(9 if len(g) == 4 else 16))
            new_grid = [0] * (9 if len(g) == 4 else 16)
            for v in new_key[1]:
                new_grid[v-1] = 1
            new_row.append(new_grid)
        new_grids.append(new_row)
    return rebuild_grid(new_grids)


enhancements = parse_file("21_input.txt")
enhancements = complete_mappings(enhancements)

initial_grid = [
        0, 1, 0,
        0, 0, 1,
        1, 1, 1,]

grid = initial_grid
for n in range(5):
    grid = cycle(grid, enhancements)
print sum(grid)
for n in range(13):
    grid = cycle(grid, enhancements)
print sum(grid)

