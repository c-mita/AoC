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
    visited = {}
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


raw_valve_map = parse_file("16_input.txt")
reduced = map_relevant_valves(raw_valve_map)

relief = find_maximum_relief(reduced)
print(relief)
