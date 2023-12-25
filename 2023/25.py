"""
As every year, today brings only a single problem to solve.

It can be solved easily by throwing the input at graph-viz with a nice
clustering engine which highlights the relevant connections nicely.
But that's unsatisfactory and no way to end the year.

We are promised that our input has exactly three edges that can be cut
to produce two disconnected subgraphs.

That means we know that every node has at least four edges (unless
the node is one of the sub-graphs in question).
So, within a subgraph, there should be at least four ways to reach
any node from any other, where each way uses a completely different
set of edges than the others. If this were not the case, then cutting
three would result in a new sub=graph, and we've been effectively
promised that that doesn't happen.

But, when we cross sub-graphs, we only have three edges to choose from.
So the above cannot happen; if we remove these three paths, we cannot
cross the graph.

So, the solution is this:
    1. Pick a point on the graph.
    2. For each other point, run a BFS to see find the quickest route
       to that target point.
    3. Remove the edges used in this walk.
    4. Repeat 2 and 3 another three times.
    5. If the fourth BFS can find a route, we know the two souce and
       target point are in the same sub-graph. Otherwise, they are in
       different sub-graphs and the edges removed contain the three
       edges to cut.
    6, Take the source and target points and the graph with the edges
       removed and walk the graph from the two points and count how
       many points can be reached from both.
    7. Multiply and print.

A nice problem that executes quickly.
We do not need to test many "target" points because the sub-graphs are
approximately equal in size, meaning each point as about a 50% chance
of being in the other subgraph.
"""


import collections
import itertools


def parse_file(filename):
    graph = collections.defaultdict(list)
    with open(filename) as f:
        for line in f:
            key, targets = line.strip().split(": ")
            for tgt in targets.split(" "):
                graph[key].append(tgt)
                graph[tgt].append(key)
    return graph


def find_cuttable_path(graph):

    def bfs(src, target, removed):
        visited = {src:None}
        to_visit = collections.deque([src])
        found = False
        while to_visit and not found:
            node = to_visit.popleft()
            for tgt in graph[node]:
                edge = tuple(sorted((node, tgt)))
                if tgt in visited or edge in removed:
                    continue
                visited[tgt] = node
                if tgt == target:
                    found = True
                    break
                to_visit.append(tgt)
        if not found:
            return []
        steps = [target]
        node = target
        while visited[node]:
            steps.append(visited[node])
            node = visited[node]
        return steps

    def path_to_edges(path):
        for p1, p2 in zip(path[:-1], path[1:]):
            yield tuple(sorted((p1, p2)))

    src = list(graph)[0]
    skippable = set()
    for target in graph:
        if target == src:
            continue
        if target in skippable:
            # we expect to find the answer quickly unless one of the subgraphs
            # is very small, so we don't expect to be here often...
            continue

        to_remove = set()
        for _ in range(4):
            path = bfs(src, target, to_remove)
            to_remove.update(path_to_edges(path))
            if not path:
                return to_remove, (src, target)
            skippable.update(path)
    raise ValueError("Could not identify cuttable edges")


def cut_graph(graph, edges_to_remove):
    cut = dict(graph)
    for v1, v2 in to_remove:
        cut[v1] = [v for v in cut[v1] if v != v2]
        cut[v2] = [v for v in cut[v2] if v != v1]
    return cut


def graph_walk(graph, start):
    to_visit = [start]
    visited = set(to_visit)
    while to_visit:
        node = to_visit.pop()
        for tgt in graph[node]:
            if tgt in visited:
                continue
            visited.add(tgt)
            to_visit.append(tgt)
    return visited


graph = parse_file("25.txt")

to_remove = [("xjb", "vgs"), ("xhg", "ljl"), ("ffj", "lkm")]
to_remove, (g1_start, g2_start) = find_cuttable_path(graph)

cut = cut_graph(graph, to_remove)
cg1 = graph_walk(cut, g1_start)
cg2 = graph_walk(cut, g2_start)
print(len(cg1) * len(cg2))
