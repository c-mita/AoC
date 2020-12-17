def parse_file(filename):
    with open(filename) as f:
        return [[(v[0], int(v[1:])) for v in l.strip().split(",")] for l in f]


def trace_path(path):
    cells = {}
    n = 0
    sx, sy = 0, 0
    directions = {"R":(1,0), "L":(-1,0),
            "U":(0,1), "D":(0,-1)}
    for d, v in path:
        px, py = directions[d]
        for x in range(v):
            n += 1
            sx, sy = sx + px, sy + py
            if (sx, sy) not in cells:
                cells[(sx, sy)] = n
    return cells


wire_paths = parse_file("03.txt")
seen = map(trace_path, wire_paths)

s1, s2 = seen
intersections = {c:s1[c] + s2[c] for c in s1 if c in s2}
min_xy = 0x7fffffff
min_d = 0x7fffffff
for (x, y), d in intersections.items():
    c = abs(x) + abs(y)
    min_xy = c if c < min_xy else min_xy
    min_d = d if d < min_d else min_d

print min_xy
print min_d
