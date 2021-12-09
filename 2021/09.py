"""
For part 2, we just perform a simple Breadth First Traversal beginning at each
local minimum point. We are explicitly told that every point that is not a 9
is part of precisely one basin, with 9s forming the barriers.
"""


import collections


def parse_file(filename):
    points = collections.defaultdict(lambda: 0x7fffffff)
    with open(filename) as f:
        for i, line in enumerate(f):
            for j, c in enumerate(line.strip()):
                points[(i, j)] = int(c)
    return points, (i+1, j+1)


def find_local_mins(points, bounds):
    my, mx = bounds
    mins = []
    for y in range(my):
        for x in range(mx):
            v = points[(y, x)]
            neighbours = ((y-1, x), (y+1, x), (y, x-1), (y, x+1))
            if all(v < points[(ny, nx)] for ny, nx in neighbours):
                mins.append((y, x))
    return mins


def walk_basin(points, root):
    basin = set()
    front = collections.deque()
    front.append(root)
    while front:
        px, py = front.popleft()
        basin.add((px, py))
        current_value = points[(px, py)]
        neighbours = {(px-1, py), (px+1, py), (px, py-1), (px, py+1)}
        neighbours -= basin
        for nx, ny in neighbours:
            n_value = points[(nx, ny)]
            if current_value <= n_value < 9:
                front.append((nx, ny))
    return basin


points, bounds = parse_file("09_input.txt")
mins = find_local_mins(points, bounds)
sum_of_mins = sum(1 + points[p] for p in mins)
print(sum_of_mins)

sizes = sorted([len(walk_basin(points, root)) for root in mins])
print(sizes[-1] * sizes[-2] * sizes[-3])
