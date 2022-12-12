import collections


def parse_file(filename):
    heights = {c:v for (c, v) in zip("abcdefghijklmnopqrstuvwxyz", range(26))}
    grid = {}
    start, target = None, None
    with open(filename) as f:
        for x, line in enumerate(f):
            for y, c in enumerate(line.strip()):
                if c == "S":
                    start = (x, y)
                    height = heights["a"]
                elif c == "E":
                    target = (x, y)
                    height = heights["z"]
                else:
                    height = heights[c]
                grid[(x, y)] = height
    return grid, start, target


def create_graph(grid):
    graph = collections.defaultdict(list)
    for (x, y), h in grid.items():
        neighbours = [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]
        for (px, py) in neighbours:
            dh = grid.get((px, py), 0x7FFFFFFF) - grid[(x, y)]
            if dh <= 1:
                graph[(x, y)].append((px, py))
    return graph


def reverse_graph(graph):
    rg = collections.defaultdict(list)
    for p, neighbours in graph.items():
        for n in neighbours:
            rg[n].append(p)
    return rg


def bfs(graph, start, target_func):
    visited = set()
    to_visit = [start]
    steps = 0
    while to_visit:
        front = set()
        for n in to_visit:
            if target_func(n):
                return steps
            front.update(graph[n])
        front -= visited
        visited |= front
        to_visit = front
        steps += 1
    raise ValueError("Could not navigate")

grid, start, target = parse_file("12_input.txt")

# Part 1
graph = create_graph(grid)
distance = bfs(graph, start, lambda x: x == target)
print(distance)

# Part 2; start at the destination and work backwards, looking for
# the first "a". Note we need to reverse the graph in this case.
reverse_graph = reverse_graph(graph)
best_a_distance = bfs(reverse_graph, target, lambda x: grid[x]==0)
print(best_a_distance)
