import collections

def parse_file(filename):
    active = []
    with open(filename) as f:
        for y, l in enumerate(f):
            for x, c in enumerate(l.strip()):
                if c == "#":
                    active.append((x, y))
    return active


def next_tile(tile, neighbour_func):
    counts = collections.defaultdict(int)
    for p in tile:
        for c in neighbour_func(p):
            counts[c] += 1
    return (k for k in counts if (k in tile and counts[k] == 1) or (k not in tile and 1 <= counts[k] < 3))


def neighbours(coord):
    x, y = coord
    n = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    return [(nx, ny) for nx, ny in n if 0 <= nx < 5 and 0 <= ny < 5]


def neighbours_recursive(coord):
    x, y, z = coord
    n = [(x-1, y, z), (x+1, y, z), (x, y-1, z), (x, y+1, z)]
    n = [(nx, ny, nz) for nx, ny, nz in n if 0 <= nx < 5 and 0 <= ny < 5 and (nx, ny) != (2, 2)]
    if x == 0: n.append((1, 2, z-1))
    if x == 4: n.append((3, 2, z-1))
    if y == 0: n.append((2, 1, z-1))
    if y == 4: n.append((2, 3, z-1))
    if x == 1 and y == 2:
        n += [(0, v, z+1) for v in range(5)]
    if x == 3 and y == 2:
        n += [(4, v, z+1) for v in range(5)]
    if x == 2 and y == 1:
        n += [(v, 0, z+1) for v in range(5)]
    if x == 2 and y == 3:
        n += [(v, 4, z+1) for v in range(5)]
    return n


def rate_tile(tile):
    r = 0
    for x, y in tile:
        p = y * 5 + x
        r += 2**p
    return r


initial_tile = tuple(parse_file("24.txt"))

seen = set()
tile = initial_tile
while tile not in seen:
    seen.add(tile)
    tile = tuple(sorted(next_tile(tile, neighbours)))
print rate_tile(tile)


tile = {(x, y, 0) for x, y in initial_tile}
for n in range(200):
    tile = set(next_tile(tile, neighbours_recursive))
print len(tile)
