test_graph = {0:[2], 1:[1], 2:[0, 3, 4], 3:[2, 4], 4:[2, 3, 6], 5:[6], 6:[4,5]}

def parse_input(filename):
    def parse_line(line):
        start, ends = line.split(" <-> ")
        start = int(start)
        ends = [int(n.strip()) for n in ends.split(", ")]
        return start, ends
    with open(filename) as f:
        return {start:ends for (start,ends) in (parse_line(l) for l in f)}


def find_reachable(graph, start):
    visited = {start}
    to_visit = list(graph[start])
    while to_visit:
        visit = to_visit.pop(0)
        if visit in visited: continue
        visited.add(visit)
        to_visit.extend(graph[visit])
    return visited

graph = parse_input("12_input.txt")
reachable = find_reachable(graph, 0)
print len(reachable)

reduced_graph = dict(graph)
groups = 0
while reduced_graph:
    groups += 1
    start = reduced_graph.keys()[0]
    reachable = find_reachable(reduced_graph, start)
    reduced_graph = {k:v for (k,v) in reduced_graph.items() if k not in reachable}
print groups
