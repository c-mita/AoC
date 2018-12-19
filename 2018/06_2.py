import re
from collections import namedtuple, deque

colour_distance = namedtuple("colour_distance", ["key", "min_distance"])

TEST_INPUT = [[1, 1], [1, 6], [8, 3], [3, 4], [5, 5], [8, 9]]

"""
Trying to be clever by using a flood fill on the grid starting from each point,
stopping when we can no longer beat any minimum distance.

Doesn't beat simple distance calculations for every grid location against every
input coordinate, and does not help with second part of problem.
"""

def get_neighbours(coord, x_range, y_range):
    x, y = coord
    next_coords = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    return [(x, y) for (x, y) in next_coords if 0 <= x < x_range and 0 <= y < y_range]


def flood_fill(grid, x_range, y_range, start_coord, key):
    #to_visit = [(start_coord, 0)]
    to_visit = deque()
    to_visit.append((start_coord, 0))
    while to_visit:
        #coord, distance = to_visit.pop(0)
        coord, distance = to_visit.popleft()
        x, y = coord
        idx = y * x_range + x
        current_candidate = grid[idx]
        if distance < current_candidate.min_distance:
            grid[idx] = colour_distance(key, distance)
            next_coords = get_neighbours(coord, x_range, y_range)
            to_visit.extend((coord, distance + 1) for coord in next_coords)
        elif distance == current_candidate.min_distance and current_candidate.key != key:
            grid[idx] = colour_distance(-1, distance)
        else:
            pass


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
#coords = TEST_INPUT

min_x = min(coords, key=lambda (x, y): x)[0]
max_x = max(coords, key=lambda (x, y): x)[0]
min_y = min(coords, key=lambda (x, y): y)[1]
max_y = max(coords, key=lambda (x, y): y)[1]

x_start, y_start = min_x - 1, min_y - 1
x_end, y_end = max_x + 1, max_y + 1
x_range, y_range = x_end - x_start, y_end - y_start

grid = [colour_distance(-2, 0x7FFFFFFF) for n in xrange(y_range * x_range)]

adjusted_coords = [(x - x_start, y - y_start) for (x, y) in coords]

current_key = 0
for coord in adjusted_coords:
    print coord, current_key
    flood_fill(grid, x_range, y_range, coord, current_key)
    current_key += 1

region_sizes = calc_regions(grid)
infinite_regions = find_infinite_regions(grid, x_range, y_range)
print region_sizes
print infinite_regions
print max(((k, v) for (k, v) in region_sizes.iteritems() if k not in infinite_regions and k != -1), key=lambda (k, v) : v)
