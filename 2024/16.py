"""
Conceptually quite straight forward.
Part 1:
    Just run Dijsktra's algorithm on the graph of (coord, direction).
    Because most of the nodes are uninteresting, it's possible to
    reduce the graph to "interesting" points and run the search on that,
    but the time saving is not worth it for the amount of code.

Part 2:
    Modify the path search to yield all shortest paths.
    Then do a DFS of this path and mark the tiles visited.
"""


import heapq


def parse_file(filename):
    grid = {}
    with open(filename) as f:
        for r, line in enumerate(f):
            for c, s in enumerate(line.strip()):
                if s in "SE.":
                    grid[(r, c)] = s
    return grid


def dijkstra(graph, start, target_coord):

    def neighbours(node):
        (cx, cy), (dx, dy) = node
        nx, ny = cx + dx, cy + dy
        if (nx, ny) in grid:
            yield ((nx, ny), (dx, dy)), 1
        yield ((cx, cy), (-dy, dx)), 1000
        yield ((cx, cy), (dy, -dx)), 1000

    distances = {start:0}
    parents = {}
    queue = []
    visited = set()

    current = start
    while current[0] != target_coord:
        current_d = distances[current]
        for node, cost in neighbours(current):
            if node in visited:
                continue
            nd = current_d + cost
            if node not in distances or nd < distances[node]:
                distances[node] = nd
                parents[node] = [current]
                heapq.heappush(queue, (nd, node))
            elif nd == distances[node]:
                parents[node].append(current)
        visited.add(current)
        if not queue:
            raise ValueError("No solution found")
        _, current = heapq.heappop(queue)
    return distances[current], parents


def walk_trace(trace, start):
    tiles = set()
    visited = set()
    def walk(key):
        # DFS where we recurse when multiple options exist in the trace
        while key in trace and key not in visited:
            visited.add(key)
            tiles.add(key[0])
            children = iter(trace[key])
            key = next(children)
            for other in children:
                walk(other)
        # make sure we add the final tile
        visited.add(key)
        tiles.add(key[0])
    walk(start)
    return len(tiles)


grid = parse_file("16.txt")

start_coord = [k for k in grid if grid[k] == "S"][0]
end_coord = [k for k in grid if grid[k] == "E"][0]
start = (start_coord, (0, 1))

lowest_score, trace = dijkstra(grid, start, end_coord)
print(lowest_score)

end = [k for k in trace if k[0] == end_coord][0]
path_sum = walk_trace(trace, end)
print(path_sum)
