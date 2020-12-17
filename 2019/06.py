def parse_file(filename):
    with open(filename) as f:
        return dict(reversed(l.strip().split(")")) for l in f)


def reverse_map(mapping):
    graph = {}
    for k, v in mapping.items():
        graph.setdefault(v, []).append(k)
    return graph


def get_transitive_deps(graph, root):
    deps = {root:set()}
    for child in graph.get(root, []):
        deps[root].add(child)
        d = get_transitive_deps(graph, child)
        deps.update(d)
        deps[root] |= d[child]
    return deps


def get_distances(graph, root, n=0):
    distances = {root:n}
    for child in graph.get(root, []):
        distances.update(get_distances(graph, child, n+1))
    return distances


def find_first_ancestor(graph, closure, root, targets):
    targets = set(targets)
    while True:
        for child in graph[root]:
            if targets <= closure[child]:
                root = child
                break
        else:
            return root


orbit_graph = parse_file("06.txt")
reverse_orbits = reverse_map(orbit_graph)

transitive_deps = get_transitive_deps(reverse_orbits, "COM")
print sum(len(v) for v in transitive_deps.values())

# we want the final node that contains both "YOU" and "SAN"
orbit_distances = get_distances(reverse_orbits, "COM")
targets = ["YOU", "SAN"]
parent = find_first_ancestor(reverse_orbits, transitive_deps, "COM", targets)
parent_distance = orbit_distances[parent]
# we subtract two, because we don't count the YOU->parent and parent->SAN edges
print sum(orbit_distances[t] - parent_distance for t in targets) - 2
