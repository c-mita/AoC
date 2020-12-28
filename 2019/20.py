import collections
import itertools


def parse_file(filename):
    cells = {}
    with open(filename) as f:
        for y, l in enumerate(f):
            for x, c in enumerate(l):
                if c == " ":
                    continue
                cells[(x, y)] = c
    return cells


def coord_neighbours((x, y)):
    return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]


def reduce_grid(cells):
    walkable = set()
    portals = collections.defaultdict(list)
    for (x, y), c in cells.items():
        if c == "#":
            continue
        if c == ".":
            walkable.add((x, y))
            continue
        pathable = False
        symbols = [c]
        for nxy in coord_neighbours((x, y)):
            if nxy not in cells:
                continue
            if cells[nxy] == ".":
                pathable = True
            if cells[nxy] not in ".#":
                symbols.append(cells[nxy])
        if pathable:
            symbol = "".join(sorted(symbols))
            portals[symbol].append((x, y))
    return walkable, portals


def calc_neighbours(walkable, portals):
    paths = collections.defaultdict(list)
    reverse_portals = {}
    minx, miny = 0x7fffffff, 0x7fffffff
    maxx, maxy = 0, 0
    for x, y in walkable:
        minx = x if x < minx else minx
        miny = x if x < miny else miny
        maxx = x if maxx < x else maxx
        maxy = x if maxy < y else maxy

    for p, v in portals.items():
        if len(v) != 2:
            continue
        v1, v2 = v
        v1adj = [xy for xy in coord_neighbours(v1) if xy in walkable][0]
        v2adj = [xy for xy in coord_neighbours(v2) if xy in walkable][0]
        portal_dir = -1 if (v1adj[0] == minx or v1adj[0] == maxx) or v1adj[1] == miny or v1adj[1] == maxx else 1
        reverse_portals[v1] = v2adj, portal_dir
        reverse_portals[v2] = v1adj, -1 * portal_dir

    for (x, y) in walkable:
        for nxy in coord_neighbours((x, y)):
            if nxy in walkable:
                paths[(x, y)].append((nxy, 0))
            if nxy in reverse_portals:
                paths[(x, y)].append(reverse_portals[nxy])
    return paths


def traverse_simple(cells, start, target):
    seen = set()
    front = {start}
    n = 0
    while target not in front:
        seen = seen.union(front)
        front = set(q[0] for q in itertools.chain.from_iterable(cells[v] for v in front))
        front -= seen
        if not front:
            raise ValueError("No valid path")
        n += 1
    return n


def traverse_complex(cells, start, target):
    start = start, 0
    target = target, 0
    front = {start}
    seen = set()
    n = 0
    while target not in front:
        if not front:
            raise ValueError("No valid path")
        seen.update(front)
        next_front = set()
        for pos, depth in front:
            for s, d in cells[pos]:
                new_depth = depth + d
                if new_depth < 0:
                    continue
                # next_front -= seen is much more expensive than this...
                if (s, new_depth) not in seen:
                    next_front.add((s, new_depth))
        front = next_front
        n += 1
    return n



cells = parse_file("20.txt")
walkable, portals = reduce_grid(cells)
cell_paths = calc_neighbours(walkable, portals)

start = [xy for xy in coord_neighbours(portals["AA"][0]) if xy in walkable][0]
end = [xy for xy in coord_neighbours(portals["ZZ"][0]) if xy in walkable][0]
print traverse_simple(cell_paths, start, end)
print traverse_complex(cell_paths, start, end)
