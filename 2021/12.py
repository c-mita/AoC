import collections

Cave = collections.namedtuple("Cave", ["name", "big"])

def parse_input(filename):
    def parse_cave_string(string):
        big = not bool(ord(string[0]) & 32)
        return Cave(string, big)

    paths = collections.defaultdict(list)
    with open(filename) as f:
        for line in f:
            a, b = line.strip().split("-")
            cave_a, cave_b = parse_cave_string(a), parse_cave_string(b)
            paths[cave_a].append(cave_b)
            paths[cave_b].append(cave_a)
    return paths


def find_paths(network, start, end):
    # we perform a depth first travesal, tracking all routes through
    def dfs(node, visited):
        if node == end:
            return 1
        if not node.big:
            visited.add(node)

        routes = 0
        for neighbour in network[node]:
            if neighbour.big or neighbour not in visited:
                routes += dfs(neighbour, visited)
        if not node.big:
            visited.remove(node)
        return routes
    return dfs(start, set())


def find_paths_with_revisit(network, start, end):
    # another DFS with a single bit of extra state to track potential revisit
    # slightly inefficient, because we will traverse routes that don't require revisits twice
    def dfs(node, visited, small_revisited):
        if node == end:
            return (0, 1) if small_revisited else (1, 0)
        if not node.big:
            visited.add(node)
        routes, routes_revisit = 0, 0
        for neighbour in network[node]:
            if neighbour.big or neighbour not in visited:
                found, found_revisit = dfs(neighbour, visited, small_revisited)
                routes += found
                routes_revisit += found_revisit
        if not node.big:
            visited.remove(node)
        if not small_revisited and not node == start:
            for neighbour in network[node]:
                if neighbour.big or neighbour not in visited:
                    found, found_revisit = dfs(neighbour, visited, 1)
                    routes_revisit += found_revisit
            # we will double count routes that didn't need to revisit a small node
            routes_revisit -= routes
        return routes, routes_revisit

    routes, routes_revisit = dfs(start, set(), 0)
    return routes + routes_revisit


network = parse_input("12_input.txt")
start = Cave("start", False)
end = Cave("end", False)
routes = find_paths(network, start, end)
print(routes)
routes = find_paths_with_revisit(network, start, end)
print(routes)
