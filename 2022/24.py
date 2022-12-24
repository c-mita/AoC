"""
The blizzards are cyclic. We compute their positions for every time interval
within this cycle (the cycle length is equal to the width of the grid for <
and > blizzards, and its height for ^ and v ones).
We can then do simple look ups to filter the available paths in a BFS walk.
"""


import collections


def parse_file(filename):
    with open(filename) as f:
        lines = f.readlines()
        start = lines[0].index(".") - 1
        end = lines[-1].index(".") - 1
        left_moving = collections.defaultdict(list)
        right_moving = collections.defaultdict(list)
        up_moving = collections.defaultdict(list)
        down_moving = collections.defaultdict(list)
        for r, line in enumerate(lines[1:-1]):
            for c, v in enumerate(line[1:-1]):
                if v == ">":
                    right_moving[r].append(c)
                elif v == "<":
                    left_moving[r].append(c)
                elif v == "^":
                    up_moving[c].append(r)
                elif v == "v":
                    down_moving[c].append(r)
        bounds = (0, 0), (len(lines) - 2, len(lines[0].strip()) - 2)
    return (-1, start), (bounds[1][0], end), bounds, right_moving, left_moving, down_moving, up_moving

def generate_blizzard_states(rows, columns, left, right, up, down):
    lefts = {}
    rights = {}
    downs = {}
    ups = {}
    for n in range(columns):
        lr = {}
        rr = {}
        for row in range(rows):
            lr[row] = set((c - n) % columns for c in left[row])
            rr[row] = set((c + n) % columns for c in right[row])
        lefts[n] = lr
        rights[n] = rr
    for n in range(rows):
        ur = {}
        dr = {}
        for column in range(columns):
            ur[column] = set((r - n) % rows for r in up[column])
            dr[column] = set((r + n) % rows for r in down[column])
        ups[n] = ur
        downs[n] = dr
    return lefts, rights, ups, downs


def walk_to_target(start, end, rows, columns, lefts, rights, ups, downs, start_time=0):
    def neighbours(pos):
        x, y = pos
        new = ((x-1, y), (x+1, y), (x, y-1), (x, y+1), (x, y))
        yield from ((x, y) for (x, y) in new if (0 <= x < rows and 0 <= y < columns) \
                or (x, y) == start or (x, y) == end)

    visited = set()
    d = start_time
    rn, cn = d % rows, d % columns
    to_visit = {(start, rn, cn)}
    while to_visit:
        d += 1
        next_visit = set()
        for pos, rn, cn in to_visit:
            if pos == end:
                return d
            rn += 1
            cn += 1
            rn %= rows
            cn %= columns
            for npos in neighbours(pos):
                nrow, ncol = npos
                # we have to permit waiting at the start and end wthout checking
                # their indices because they may lay outside of the bounding box
                if (npos != start and npos != end) and (
                        ncol in lefts[cn][nrow] \
                        or ncol in rights[cn][nrow] \
                        or nrow in ups[rn][ncol] \
                        or nrow in downs[rn][ncol]):
                    continue
                next_visit.add((npos, rn, cn))
        next_visit -= visited
        visited |= next_visit
        to_visit = next_visit
    raise ValueError("No route found :(")


start, end, bounds, right, left, down, up = parse_file("24_input.txt")
rows, columns = bounds[1]
lefts, rights, ups, downs = generate_blizzard_states(rows, columns, left, right, up, down)

target = end[0] - 1, end[1]
# walk to the cell above the target because it's in bounds
d1 = walk_to_target(start, target, rows, columns, lefts, rights, ups, downs)
print(d1)

return_target = start[0] + 1, start[1]
d2 = walk_to_target(end, return_target, rows, columns, lefts, rights, ups, downs, start_time=d1)
d3 = walk_to_target(start, target, rows, columns, lefts, rights, ups, downs, start_time=d2)
print(d3)
