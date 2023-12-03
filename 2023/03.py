def parse_file(filename):
    grid = {}
    with open(filename) as f:
        for r, line in enumerate(f):
            for c, symbol in enumerate(line.strip()):
                if symbol in "0123456789":
                    symbol = int(symbol)
                if symbol != ".":
                    grid[(r, c)] = symbol
    return grid


def extract_number(grid, coord):
    """Given a coord for the grid, identify the number it is part of and the
    coordinates used by that number."""
    r, c = coord
    if (r, c) not in grid or not isinstance(grid[(r, c)], int):
        raise ValueError("Bad coord")
    while (r, c-1) in grid and isinstance(grid[(r, c-1)], int):
        c -= 1
    n = 0
    marked = []
    while (r, c) in grid and isinstance(grid[(r, c)], int):
        marked.append((r, c))
        n *= 10
        n += grid[(r, c)]
        c += 1
    return n, marked


def identify_relevant(grid):
    relevant = []
    for ((r, c), v) in grid.items():
        if not isinstance(v, int):
            neighbours = [
                    (r-1, c-1), (r-1, c), (r-1, c+1),
                    (r, c-1), (r, c+1),
                    (r+1, c-1), (r+1, c), (r+1, c+1)
            ]
            seen = set()
            for n in neighbours:
                if n in seen:
                    continue
                if n in grid and isinstance(grid[n], int):
                    value, marked = extract_number(grid, n)
                    seen.update(marked)
                    relevant.append(value)
    return relevant


def identify_gears(grid):
    gears = []
    for ((r, c), v) in grid.items():
        if v != "*":
            continue
        neighbours = [
                (r-1, c-1), (r-1, c), (r-1, c+1),
                (r, c-1), (r, c+1),
                (r+1, c-1), (r+1, c), (r+1, c+1)
        ]
        seen = set()
        relevant = []
        for n in neighbours:
            if n in seen:
                continue
            if n in grid and isinstance(grid[n], int):
                value, marked = extract_number(grid, n)
                seen.update(marked)
                relevant.append(value)
        if len(relevant) == 2:
            gears.append(relevant[0] * relevant[1])
    return gears


grid = parse_file("03.txt")
relevant = identify_relevant(grid)
print(sum(relevant))

gears = identify_gears(grid)
print(sum(gears))
