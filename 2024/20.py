"""
Identify the distance to the exit from every point on the track.
Find potential shortcuts and output the distance saved by taking them
via the simple calculation:
  saving = distance[start_shortcut] - distance[end_shortcut] - shortcut_length

Part 2 is the same, but we look at every "shortcut target" point within 20 steps
according to the Manhatten metric.

Not fast, but it works.
"""


def parse_file(filename):
    grid = {}
    with open(filename) as f:
        for r, line in enumerate(f):
            for c, s in enumerate(line.strip()):
                if s != "#":
                    grid[(r, c)] = s
    return grid


def neighbours(p):
        px, py = p
        yield px-1, py
        yield px+1, py
        yield px, py-1
        yield px, py+1


def find_distances(grid, target):
    to_visit = [target]
    visited = set(to_visit)
    distances = {}
    n = 0
    while to_visit:
        front = []
        for v in to_visit:
            distances[v] = n
            for p in neighbours(v):
                if p not in grid or p in visited:
                    continue
                front.append(p)
                visited.add(p)

        to_visit = front
        n += 1
    return distances


def two_step_shortcut(p, distances):
    for wall in (k for k in neighbours(p) if k not in distances):
        for target in (k for k in neighbours(wall) if k in distances):
            saving = distances[p] - 2 - distances[target]
            if saving > 0:
                yield saving, target


BIG_DELTAS = [(x, y) for x in range(-20, 21) for y in range(-20, 21) if abs(x) + abs(y) <= 20]


def twenty_step_shortcut(p, distances):
    px, py = p
    for dx, dy in BIG_DELTAS:
        nx, ny = px + dx, py + dy
        if (nx, ny) not in distances:
            continue
        saving = distances[p] - abs(dx) - abs(dy) - distances[(nx, ny)]
        if saving > 0:
            yield saving, (nx, ny)


def find_shortcuts(distances, shortcut_func):
    for p in distances:
        for saving, target in shortcut_func(p, distances):
            yield saving, (p, target)


grid = parse_file("20.txt")
end = [k for k in grid if grid[k] == "E"][0]
start = [k for k in grid if grid[k] == "S"][0]
distances = find_distances(grid, end)

savings = find_shortcuts(distances, two_step_shortcut)
worth_while = [(saving, p) for (saving, p) in savings if saving >= 100]
print(len(worth_while))

savings = find_shortcuts(distances, twenty_step_shortcut)
worth_while = [(saving, p) for (saving, p) in savings if saving >= 100]
print(len(worth_while))
