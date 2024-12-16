"""
Conceptually quite straight forward.
Part 1:
    Condense the input grid to a weighted graph where the vertices are
    "junction" points with a direction (every junction gives four
    vertices, one for each cardinal direction). The start and end points
    yield another four vertices each.
    Then we just run Dijkstra's algorithm.

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


def reduce_grid(grid):
    graph = {}
    interesting_points = set()
    for k, v in grid.items():
        if v == "E" or v == "S":
            interesting_points.add(k)
            continue
        px, py = k
        u = (px-1, py) in grid
        d = (px+1, py) in grid
        l = (px, py-1) in grid
        r = (px, py+1) in grid
        if (u and l) or (d and l) or (u and r) or (d and r):
            interesting_points.add(k)

    for k in interesting_points:
        px, py = k
        for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            steps = 1
            graph[k, (dx, dy)] = []
            nx = px + dx
            ny = py + dy
            while (nx, ny) not in interesting_points and (nx, ny) in grid:
                nx += dx
                ny += dy
                steps += 1
            if (nx, ny) in grid:
                graph[(k, (dx, dy))].append((((nx, ny), (dx, dy)), steps))

    for coord, direction in graph:
        dx, dy = direction
        graph[(coord, direction)].append(
                ((coord, (-dy, dx)), 1000),
        )
        graph[(coord, direction)].append(
                ((coord, (dy, -dx)), 1000),
        )
    return graph


def dijkstra(graph, start, target_coord):
    distances = {start:0}
    parents = {}
    queue = []
    visited = set()

    current = start
    while current[0] != target_coord:
        current_d = distances[current]
        for node, cost in graph[current]:
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
    """Walk every tile in every route starting from the given "end" point.

    We add every tile to a set and count that size to handle "overlaps".
    Some paths overlap each other and we don't want to double count
    those tiles. This is an easy way to achieve that.
    """
    visited = set()
    tiles = set()

    def walk(node):
        # Recurse on every step because it's easier than looping
        # and recursing only when given a branch.
        if node in visited:
            return
        tiles.add(node[0])
        visited.add(node)
        if node not in trace:
            return
        nx, ny = node[0]
        for child in trace[node]:
            cx, cy = child[0]
            dx = 0 if cx == nx else (cx - nx) / abs(cx - nx)
            dy = 0 if cy == ny else (cy - ny) / abs(cy - ny)
            px, py = nx, ny
            while (px, py) != (cx, cy):
                tiles.add((px, py))
                px += dx
                py += dy
            walk(child)

    walk(start)
    return len(tiles)


grid = parse_file("16.txt")
graph = reduce_grid(grid)

start_coord = [k for k in grid if grid[k] == "S"][0]
end_coord = [k for k in grid if grid[k] == "E"][0]
start = (start_coord, (0, 1))

lowest_score, trace = dijkstra(graph, start, end_coord)
print(lowest_score)

end = [k for k in trace if k[0] == end_coord][0]
path_sum = walk_trace(trace, end)
print(path_sum)
