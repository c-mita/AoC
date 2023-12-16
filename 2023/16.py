"""
Just walk the light paths as described. Loops will occur so track
where we've been and how we're oriented.

Part 2 can be solved easily enough by just trying all paths.
It's not the fastest; maybe it could be optimised by identifying
common patterns across different runs, but that would be complicated.

Still < 5 seconds on a laptop.
"""


def parse_file(filename):
    space = {}
    with open(filename) as f:
        for r, line in enumerate(f):
            for c, s in enumerate(line.strip()):
                space[(r, c)] = s
    return space


def next_steps(pos, direction, space):
    def dir_changes(symbol, direction):
        dx, dy = direction
        if symbol == ".":
            yield dx, dy
        elif symbol == "-":
            if dx == 0:
                yield dx, dy
            else:
                yield (0, -1)
                yield (0, 1)
        elif symbol == "|":
            if dy == 0:
                yield dx, dy
            else:
                yield (-1, 0)
                yield (1, 0)
        elif symbol not in ["/", "\\"]:
            raise ValueError("Bad symbol %s" % symbol)
        else:
            reverse = symbol == "/"
            yield (-dy, -dx) if reverse else (dy, dx)

    symbol = space[pos]
    px, py = pos
    for dx, dy in dir_changes(symbol, direction):
        yield (px + dx, py + dy), (dx, dy)


def illuminate(space, start):
    seen = set()
    to_move = [start]
    p, d = start
    illuminated = set([p])
    while to_move:
        p, d = to_move.pop()
        for np, nd in next_steps(p, d, space):
            if np not in space:
                continue
            if (np, nd) in seen:
                continue
            seen.add((np, nd))
            illuminated.add(np)
            to_move.append((np, nd))
    return illuminated


def start_points(space):
    max_r = max(k[0] for k in space)
    max_c = max(k[1] for k in space)
    for c in range(max_c+1):
        yield (0, c), (1, 0)
        yield (max_r, c), (-1, 0)
    for r in range(max_r+1):
        yield (r, 0), (0, 1)
        yield (r, max_c), (0, -1)


space = parse_file("16.txt")
start = (0, 0), (0, 1)
illuminated = illuminate(space, start)
print(len(illuminated))

best = max(len(illuminate(space, start)) for start in start_points(space))
print(best)
