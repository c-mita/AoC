import collections
import itertools



def parse_file(filename):
    active = set()
    with open(filename) as f:
        for x, l in enumerate(f):
            for y, c in enumerate(l.strip()):
                if c == "#":
                    active.add((x, y))
    return active


def calc_neighbours_3d(coord):
    x, y, z = coord
    product = itertools.product([x-1, x, x+1], [y-1, y, y+1], [z-1, z, z+1])
    return [v for v in product if v != coord]


def calc_neighbours_4d(coord):
    x, y, z, w = coord
    product = itertools.product(
            [x-1, x, x+1], [y-1, y, y+1], [z-1, z, z+1], [w-1, w, w+1])
    return [v for v in product if v != coord]


def cycle(state, neighbour_func):
    n_counts = collections.defaultdict(int)
    for c in state:
        for n in neighbour_func(c):
            n_counts[n] += 1
    new_state = set()
    for n, v in n_counts.items():
        if n in state and 2 <= v < 4:
            new_state.add(n)
        elif n not in state and v == 3:
            new_state.add(n)
    return new_state


TEST_STATE = {(0,1), (1,2), (2,0), (2,1), (2,2)}
initial_state = TEST_STATE
initial_state = parse_file("17.txt")

state = set((x, y, 0) for (x, y) in initial_state)
for n in range(6):
    state = cycle(state, calc_neighbours_3d)
print len(state)

state = set((x, y, 0, 0) for (x, y) in initial_state)
for n in range(6):
    state = cycle(state, calc_neighbours_4d)
print len(state)
