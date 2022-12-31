"""
Part 1:
    The first step is to reduce the graph to only consider the relevant nodes.
    Create a weighted graph of the valves that have non-zero flow values - a dumb
    BFS started from each relevant valve (and the starting point) is enough.

    Then we perform a DFS over this graph, remembering the best "relief" value
    we've seen.

Part 2:
    The two entities (the elephant and us) will activate different valves, so
    we can think about applying part 1 to disjoint subsets of the valve set.
    A slight adjustment to part 1 can give us a map of the best possible
    outcome for a given valve set walked (usnig the same DFS walk, but storing
    things a little differently), we then consider combinations of the elements
    of the powerset of the valve set (filtering out things that are not in the
    solution set) and find the best pairing - there's only about 10  million
    pairs, which is high, but not catastrophically so.
"""


import itertools
import re


def parse_file(filename):
    valve_map = {}
    with open(filename) as f:
        for line in f:
            flow_rate = int(re.findall("[0-9]+", line)[0])
            valves = re.findall("[A-Z][A-Z]", line)
            valve_map[valves[0]]= (flow_rate, valves[1:])
    return valve_map


def map_relevant_valves(valve_map, start_pos="AA"):
    relevant = {}

    def bfs(start):
        visited = set()
        to_visit = [start]
        walkable = []
        d = -1
        while to_visit:
            d += 1
            next_visit = set()
            for v in to_visit:
                visited.add(v)
                fr, neighbours = valve_map[v]
                if fr and d:
                    walkable.append(((v, fr), d))
                next_visit.update(neighbours)
            next_visit -= visited
            to_visit = next_visit
        return walkable

    for start_valve, (flow_rate, neighbours) in valve_map.items():
        if flow_rate or start_valve == start_pos:
            relevant[start_valve] = bfs(start_valve)
    return relevant


def find_maximum_relief(valve_map, start_pos = "AA"):
    valves_seen = set()
    def dfs(pos, time, flow):
        valves_seen.add(pos)
        totals = []
        for (valve, rate), distance in valve_map[pos]:
            if valve in valves_seen:
                continue
            ntime = time - 1 - distance
            if ntime < 0:
                continue
            nflow = flow + rate
            score = dfs(valve, ntime, nflow)
            totals.append((score[0] + rate * ntime, score[1]))
        best = max(totals, default=(0, ()))
        score = best[0]
        chain = (pos,) + best[1]
        valves_seen.remove(pos)
        return score, chain
    v = dfs(start_pos, 30, 0)
    return v


def calculate_relief(valve_map, start_pos = "AA", time=30):
    visited = {}
    valves_seen = set()
    # walk all possible valve openings and record the best for
    # each set of possible valves that can be opened in time
    def dfs(pos, chain, relief, time):
        vkey = tuple(sorted(valves_seen))
        if vkey in visited:
            vrelief, vchain = visited[vkey]
            if relief < vrelief:
                return
        visited[vkey] = (relief, chain)
        for (valve, rate), distance in valve_map[pos]:
            if valve in valves_seen:
                continue
            ntime = time - 1 - distance
            if ntime < 0:
                continue
            nrelief = relief + rate * ntime
            valves_seen.add(valve)
            dfs(valve, chain + (valve,), nrelief, ntime)
            valves_seen.remove(valve)
    dfs(start_pos, (start_pos,), 0, time)
    return visited


def powerset(it):
    s = list(it)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))


raw_valve_map = parse_file("16_input.txt")
reduced = map_relevant_valves(raw_valve_map)

relief = find_maximum_relief(reduced)
print(relief)
options = calculate_relief(reduced)
best = max(options, key=lambda k:options[k][0])
print(options[best])

options = calculate_relief(reduced, time=26)
valves = list(reduced.keys())
valves = [v for v in valves if v != "AA"]
ps_valves = [set(v) for v in powerset(valves)]
ps_valves = [(v, tuple(sorted(v))) for v in ps_valves if tuple(sorted(v)) in options]
best, bvs1, bvs2 = 0, None, None
for (vs1, k1), (vs2, k2) in itertools.combinations(ps_valves, 2):
    if not vs1.isdisjoint(vs2):
        continue
    s = options[k1][0] + options[k2][0]
    if best < s:
        best, bvs1, bvs2 = s, options[k1][1], options[k2][1]

print(best, bvs1, bvs2)
