def parse_file(filename):
    with open(filename) as f:
        return list(map(int, (l for l in f)))


def find_deltas(joltages):
    deltas = {0:0, 1:0, 2:0, 3:0}
    joltages = [0] + joltages + [joltages[-1] + 3]
    for v1, v2 in zip(joltages[:-1], joltages[1:]):
        d = v2 - v1
        deltas[d] += 1
    return deltas


def count_paths(values):
    paths = {0:1}
    for v in values:
        s = paths.setdefault(v-1, 0) + paths.setdefault(v-2, 0) + paths.setdefault(v-3, 0)
        paths[v] = s
    return paths[values[-1]]


adapters = parse_file("10.txt")
adapters = sorted(adapters)
deltas = find_deltas(adapters)
print deltas[1] * deltas[3]
print count_paths(adapters + [adapters[-1] + 3])
