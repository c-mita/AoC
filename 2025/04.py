"""
Simple enough. For part 1 just look at every cell's neighbours.
For part 2 we could iteratively sweep the grid and remove any
cell that satisifes the condition; it's not too slow (~0.5 seconds).

Alternatively, write down the number of "neighbours" each populated
cell has. Then remove those that satisfy the condition (<4 neighbours)
and decrement the count for each of its neighbours. Repeat until we
remove nothing. This is quite a bit faster since we only inspect the
relevant cells at each iteration step (~0.1s).
"""

def parse_input(data):
    grid = {}
    if type(data) == str:
        data = data.split()
    for r, line in enumerate(data):
        line = line.strip()
        for c, s in enumerate(line):
            grid[(r, c)] = s == "@"
    return grid


def neighbours(cell):
    r, c = cell
    yield (r-1, c-1)
    yield (r-1, c)
    yield (r-1, c+1)
    yield (r, c-1)
    yield (r, c+1)
    yield (r+1, c-1)
    yield (r+1, c)
    yield (r+1, c+1)


def count_neighbours(grid, cell):
    return sum(grid.get(n, 0) for n in neighbours(cell))


def valid_positions(grid):
    valid = []
    for cell in grid:
        if grid[cell] and count_neighbours(grid, cell) < 4:
            valid.append(cell)
    return valid


def keep_removing_all_valid(grid):
    # iteratively remove all "removable" rolls from the grid
    grid = dict(grid)
    to_remove = valid_positions(grid)
    removed = 0
    while to_remove:
        removed += len(to_remove)
        for k in to_remove:
            grid[k] = False
        to_remove = valid_positions(grid)
    return removed


def remove_all_valid(grid):
    counts = {k:count_neighbours(grid, k) for k in grid if grid[k]}
    removed = 0
    to_remove = [k for k in counts if counts[k] < 4]
    while to_remove:
        removed += len(to_remove)
        for k in to_remove:
            del counts[k]
            for n in neighbours(k):
                if n not in counts or not counts[n]:
                    continue
                counts[n] -= 1
        to_remove = [k for k in counts if counts[k] < 4]
    return removed


TEST_INPUT = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""

test_world = parse_input(TEST_INPUT)
with open("04.txt") as f:
    world = parse_input(f)
valid = valid_positions(world)
print(len(valid))

#fully_removable = keep_removing_all_valid(world)
#print(fully_removable)

fully_removable = remove_all_valid(world)
print(fully_removable)
