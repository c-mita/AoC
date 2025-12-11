"""
Very simple. Just a DFS walk over the graph.

Part 1 can be a vanilla DFS search.
Part 2 requires some caching. We note that the graph is acyclic so it
doesn't matter how we reached a given node, we can just store the
number of ways the target can be reached from there.

Then just multiple the ways to perform each subcomponent of the desired
path.
"""


def parse_data(data):
    graph = {}
    if type(data) == str:
        data = data.split("\n")
    for line in data:
        line = line.strip()
        if not line:
            continue
        nodes = line.split(" ")
        node = nodes[0][:-1] # remove trailing ":"
        graph[node] = nodes[1:]
    return graph


def check_acyclic(graph):
    def walk(start, graph):
        graph = dict(graph)
        to_visit = [start]
        visited = set(to_visit)
        while to_visit:
            current = to_visit.pop()
            if current not in graph:
                graph[current] = []
            for child in graph[current]:
                if child == start:
                    raise ValueError("Graph has a cycle")
                if child in visited:
                    continue
                visited.add(child)
                to_visit.append(child)
        return

    for node in graph:
        walk(node, graph)


def count_paths(graph, start, target):
    node_keys = {}
    nodes = set()
    for node, targets in graph.items():
        nodes.add(node)
        nodes.update(targets)

    for i, node in enumerate(nodes):
        node_keys[node] = 1 << i

    cache = {}
    def dfs(current):
        if current in cache:
            return cache[current]
        if current == target:
            return 1
        if current not in graph:
            return 0
        routes = 0
        for child in graph[current]:
            routes += dfs(child)
        cache[current] = routes
        return routes

    return dfs(start)


TEST_DATA = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

test_graph = parse_data(TEST_DATA)

with open("11.txt") as f:
    graph = parse_data(f)

#graph = test_graph
check_acyclic(graph)

paths = count_paths(graph, start="you", target="out")
print(paths)

# Only one of these routes will be possible, the other will give zero
routes = [("svr", "dac", "fft", "out"), ("svr", "fft", "dac", "out")]
total = 0
for route in routes:
    route_total = 1
    for start, end in zip(route[:-1], route[1:]):
        if route_total:
            route_total *= count_paths(graph, start=start, target=end)
    total += route_total
print(total)
