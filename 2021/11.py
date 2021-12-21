TEST_GRID = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""

INPUT_GRID = """
6744638455
3135745418
4754123271
4224257161
8167186546
2268577674
7177768175
2662255275
4655343376
7852526168
"""


import collections


def parse_grid(grid_string):
    grid = {}
    for j, l in enumerate(grid_string.split("\n")):
        for i, c in enumerate(l.strip()):
            grid[(i, j)] = int(c)
    return grid


def step_grid(grid):
    to_flash = collections.deque()
    flashed = set()
    next_grid = {}
    for (i, j), v in grid.items():
        next_grid[(i, j)] = grid[(i, j)] + 1
        if v >= 9:
            to_flash.append((i, j))
            flashed.add((i, j))

    while to_flash:
        i, j = to_flash.popleft()
        for (x, y) in [(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)]:
            if (x, y)  in next_grid:
                next_grid[(x, y)] += 1
                if next_grid[(x, y)] >= 10 and (x, y) not in flashed:
                    to_flash.append((x, y))
                    flashed.add((x, y))
    for (i, j) in flashed:
        next_grid[(i, j)] = 0
    return len(flashed), next_grid


grid = parse_grid(INPUT_GRID)
flash_count = 0
for n in range(100):
    c, grid = step_grid(grid)
    flash_count += c
print(flash_count)

grid = parse_grid(INPUT_GRID)
flashes = 0
n = 0
while flashes != len(grid):
    flashes, grid = step_grid(grid)
    n += 1
print(n)
