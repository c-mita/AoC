import collections


"""
For part 2, just run the same Dijkstra's Algorithm code on a calculated "scaled" grid.
It's not the fastest solution, but simple enough.

It's probably possible to be clever by precalculating routes through individual tiles or something.
"""

class ScaledGrid:
    def __init__(self, grid, scale):
        self.grid = grid
        self.scale = scale
        self.max_x = 0
        self.max_y = 0
        for key in grid:
            x, y = key
            if x > self.max_x: self.max_x = x
            if y > self.max_y: self.max_y = y
        self.size_x = self.max_x + 1
        self.size_y = self.max_y + 1
        self.max_sx = (self.size_x) * self.scale - 1
        self.max_sy = (self.size_y) * self.scale - 1


    def __iter__(self):
        return ((x, y) for x in range(self.max_sx) for y in range(self.max_sy))


    def __contains__(self, key):
        x, y = key
        return 0 <= x <= self.max_sx and 0 <= y <= self.max_sy


    def __getitem__(self, key):
        if not self.__contains__(key):
            raise KeyError(key)
        x, y  = key
        mx, my = int(x / self.size_x), int(y / self.size_y)
        ox, oy = x % self.size_x, y % self.size_y

        ov = self.grid[ox, oy]
        # move the range from [1-9] to [0-8] and use modular arithmetic
        v = ov - 1
        v += mx + my
        return v % 9 + 1


def parse_input(filename):
    grid = {}
    with open(filename) as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line.strip()):
                grid[(y, x)] = int(c)
    return grid, (y, x)


def minimum_walk(start_pos, end_pos, grid):
    distances = collections.defaultdict(lambda: 0x7FFFFFFF)
    distances[start_pos] = 0
    visited = set()
    relevant_nodes = set([start_pos])

    def neighbours(position, grid):
        x, y = position
        positions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        return [p for p in positions if p in grid]

    current = start_pos
    while not current == end_pos:
        cdistance = distances[current]
        for node in neighbours(current, grid):
            if node in visited:
                continue
            relevant_nodes.add(node)
            delta = grid[node]
            nd = cdistance + delta
            if nd < distances[node]:
                distances[node] = nd
        visited.add(current)
        relevant_nodes.remove(current)
        current = min(relevant_nodes, key=lambda k: distances[k])
    return distances[end_pos]


grid, (max_x, max_y) = parse_input("15_input.txt")
min_distance = minimum_walk((0, 0), (max_x, max_y), grid)
print(min_distance)

scaled_grid = ScaledGrid(grid, 5)
min_distance = minimum_walk((0, 0), (scaled_grid.max_sx, scaled_grid.max_sx), scaled_grid)
print(min_distance)
