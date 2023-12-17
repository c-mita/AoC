"""
Just use Dijkstra's Algorithm on the graph with nodes:
(coordinate, direction, steps)

The problem logic is encapsulated in the function to get the next states
given the current node; the core path finding logic does not need to be
changed between Part 1 and 2.

Part 1 could probably benefit from stricter checks; maybe we can cull some
choices by checking "remaining steps" versus previous attempts?
Part 2 seems less likely to benefit from such analysis however.

Unfortunately, completing both parts takes a total of ~6-7 seconds of runtime.
"""


import heapq


def parse_file(filename):
    graph = {}
    with open(filename) as f:
        for r, line in enumerate(f):
            line = line.strip()
            for c, s in enumerate(line):
                graph[(r, c)] = int(s)
    return graph


def dijkstra(graph, start, targets, neighbour_func):
    distances = {start:0}
    queue = []
    visited = set()

    current = start
    while current not in targets:
        cd = distances[current]
        for node, cost in neighbour_func(graph, current):
            if node in visited:
                continue
            nd = cd + cost
            if node not in distances or nd < distances[node]:
                distances[node] = nd
                heapq.heappush(queue, (nd, node))
        visited.add(current)
        _, current = heapq.heappop(queue)
    return distances[current]


def crucible_neighbour(graph, node):
    pos, direction, steps_remaining = node
    def directions():
        allowed_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in allowed_directions:
            if d[0] == -direction[0] and d[1] == -direction[1]:
                continue
            if d == direction:
                if steps_remaining:
                    yield (d, steps_remaining-1)
            else:
                yield (d, 2)

    px, py = pos
    for (dx, dy), s in directions():
        nx, ny = px+dx, py+dy
        if (nx, ny) in graph:
            yield ((nx, ny), (dx, dy), s), graph[(nx, ny)]


def ultra_crucible_neighbour(graph, node):
    pos, direction, steps = node
    def directions():
        if steps < 4:
            yield direction, steps+1
            return
        allowed_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in allowed_directions:
            if d == (-direction[0], -direction[1]):
                continue
            if d == direction:
                if steps < 10:
                    yield (d, steps+1)
            else:
                yield (d, 1)

    px, py = pos
    for (dx, dy), s in directions():
        nx, ny = px+dx, py+dy
        if (nx, ny) in graph:
            yield ((nx, ny), (dx, dy), s), graph[(nx, ny)]


graph = parse_file("17.txt")
target = max(k[0] for k in graph), max(k[1] for k in graph)

targets = [(target, (1, 0), i) for i in range(3)]
targets += [(target, (0, 1), i) for i in range(3)]
start = ((0, 0), (0, 0), 2)

heat_loss = dijkstra(graph, start, targets, crucible_neighbour)
print(heat_loss)

ultra_targets = set([(target, (1, 0), i) for i in range(4, 11)])
ultra_targets.update((target, (0, 1), i) for i in range(4, 11))
ultra_start = ((0, 0), (0, 0), (10))

ultra_heat_loss = dijkstra(graph, ultra_start, ultra_targets, ultra_crucible_neighbour)
print(ultra_heat_loss)
