"""
Part 1 is just a flood fill algorithm.

For part 2 we add some logic to detect corners, noting that for simple
polygons "n_corners == n_edges".

Identifying corners is a bit messy; the code will output duplicate corners
some of the time and different query points will output the overlapping corners.
So we shove them into a set and check the length.

To handle the "overlapping" case of a single "corner point" actually being
two distinct corners, we add a "direction" parameter to each corner.

This catches this case:
    BBBB
    BBAB
    BABB
    BBBB
"B" should have 12 edges, not 10
"""


def parse_file(filename):
    grid = {}
    with open(filename) as f:
        for r, l in enumerate(f):
            for c, s in enumerate(l.strip()):
                grid[(r, c)] = s
    return grid


def find_regions(grid):
    visited = set()
    regions = []

    def neighbours(p):
        yield p[0] - 1, p[1]
        yield p[0] + 1, p[1]
        yield p[0], p[1] - 1
        yield p[0], p[1] + 1

    def find_corners(p, v):
        """
        Returns all corners at the given point.
        The top-left corner shares its coordinate with the point.
        The corners are "directed" with a vector pointing "inwards".
        Will output repeats because we're not clever about checking
        possible conditions.
        """
        DR = (1, 1)
        UR = (-1, 1)
        DL = (1, -1)
        UL = (-1, -1)
        row, col = p
        corners = 0
        l = grid.get((row, col - 1), None) == v
        r = grid.get((row, col + 1), None) == v
        u = grid.get((row - 1, col), None) == v
        d = grid.get((row + 1, col), None) == v
        lu = grid.get((row - 1, col - 1), None) == v
        ru = grid.get((row - 1, col + 1), None) == v
        ld = grid.get((row + 1, col - 1), None) == v
        rd = grid.get((row + 1, col + 1), None) == v

        if not l and not r and not u and not d:
            yield row, col, DR
            yield row, col+1, DL,
            yield row+1, col, UR
            yield row+1, col+1, UL

        if not l and r and not u:
            yield row, col, DR
        if not l and r and not d:
            yield row+1, col, UR
        if l and not r and not u:
            yield row, col+1, DL
        if l and not r and not d:
            yield row+1, col+1, UL

        if not u and d and not l:
            yield row, col, DR
        if not u and d and not r:
            yield row, col+1, DL
        if u and not d and not l:
            yield row+1, col, UR
        if u and not d and not r:
            yield row+1, col+1, UL

        if l and u and not lu:
            yield row, col, DR
        if l and d and not ld:
            yield row+1, col, UR
        if r and u and not ru:
            yield row, col+1, DL
        if r and d and not rd:
            yield row+1, col+1, UL

    def walk_region(start):
        area = 0
        perimeter = 0
        corners = set()
        value = grid[start]
        to_walk = [start]
        while to_walk:
            p = to_walk.pop()
            if p in visited:
                continue
            visited.add(p)
            area += 1
            corners.update(find_corners(p, value))
            for n in neighbours(p):
                if n not in grid or grid[n] != value:
                    perimeter += 1
                else:
                    to_walk.append(n)
        edges = len(corners)
        return value, (area, perimeter, edges)

    for p in grid:
        if p not in visited:
            regions.append(walk_region(p))
    return regions


grid = parse_file("12.txt")
regions = find_regions(grid)

s = 0
t = 0
for region_data in regions:
    value, (area, perimeter, edges) = region_data
    s += area * perimeter
    t += area * edges
print(s)
print(t)
