"""
Didn't know about a clique, but it's exactly what we're looking for
(a subgraph where every vertex is connected to every other).

Part 2 is just implementing the basic form of the Bron-Kerbosch algorithm
from Wikipedia which finds all maximal cliques (we then return the biggest).
It's more than good enough for our purposes.
"""


import itertools


def parse_file(filename):
    with open(filename) as f:
        return [tuple(line.strip().split("-")) for line in f]


def build_graph(connections):
    graph = {}
    for left, right in connections:
        if left not in graph:
            graph[left] = []
        if right not in graph:
            graph[right] = []
        graph[left].append(right)
        graph[right].append(left)
    return graph


def find_3_cliques(graph):
    visited = set()
    for node in graph:
        for c1, c2 in itertools.combinations(graph[node], 2):
            if c2 in graph[c1]:
                v = tuple(sorted((node, c1, c2)))
                if v not in visited:
                    yield v
                visited.add(v)


def find_maximal_cliques(graph):
    def rec(clique, considered, excluded):
        if not excluded and not considered:
            yield list(sorted(clique))
        for v in list(considered):
            clique.append(v)
            neighbours = set(graph[v])
            yield from rec(
                    clique,
                    considered & neighbours,
                    excluded & neighbours
            )
            clique.pop()
            considered.remove(v)
            excluded.add(v)
    yield from rec([], set(graph.keys()), set())


data = parse_file("23.txt")
graph = build_graph(data)

relevant = []
for group in find_3_cliques(graph):
    for v in group:
        if v.startswith("t"):
            relevant.append(group)
            break
print(len(relevant))

print(",".join(max(find_maximal_cliques(graph), key=len)))
