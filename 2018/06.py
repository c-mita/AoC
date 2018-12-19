import re
from collections import namedtuple


colour_distance = namedtuple("colour_distance", ["key", "min_distance"])

TEST_INPUT = [[1, 1], [1, 6], [8, 3], [3, 4], [5, 5], [8, 9]]


def calc_regions(grid):
    key_counts = {}
    for c in grid:
        key_counts[c.key] = key_counts.get(c.key, 0) + 1
    return key_counts


def find_infinite_regions(grid, x_range, y_range):
    keys = set()
    for c in grid[:x_range] + grid[x_range * (y_range-1):]:
        keys.add(c.key)

    for c in grid[::x_range] + grid[x_range-1::x_range]:
        keys.add(c.key)

    return keys


with open("06_input.txt") as f:
    coords = [map(int, re.findall("\d+", coord.strip())) for coord in f.readlines()]

min_x = min(coords, key=lambda (x, y): x)[0]
max_x = max(coords, key=lambda (x, y): x)[0]
min_y = min(coords, key=lambda (x, y): y)[1]
max_y = max(coords, key=lambda (x, y): y)[1]

x_start, y_start = min_x - 1, min_y - 1
x_end, y_end = max_x + 1, max_y + 1
x_range, y_range = x_end - x_start, y_end - y_start

adjusted_coords = [(x - x_start, y - y_start) for (x, y) in coords]

min_grid = [None] * (x_range * y_range)
sum_grid = [None] * (x_range * y_range)

for y in xrange(y_range):
    for x in xrange(x_range):
        idx = y * x_range + x
        coord_distances = [abs(x - cx) + abs(y - cy) for (cx, cy) in adjusted_coords]
        sum_grid[idx] = sum(coord_distances)
        sorted_distances = sorted(coord_distances)
        if sorted_distances[0] == sorted_distances[1] or sorted_distances[0] == sorted_distances[2]:
            min_grid[idx] = colour_distance(-1, distance)
        else:
            key, distance = min(enumerate(coord_distances), key=lambda v:v[1])
            min_grid[idx] = colour_distance(key, distance)


region_sizes = calc_regions(min_grid)
infinite_regions = find_infinite_regions(min_grid, x_range, y_range)
print region_sizes
print infinite_regions
print max(((k, v) for (k, v) in region_sizes.iteritems() if k not in infinite_regions and k != -1), key=lambda (k, v) : v)

print len(filter(lambda v: v < 10000, sum_grid))
