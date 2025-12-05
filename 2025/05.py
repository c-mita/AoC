"""
Part 1 is just do the thing. Collapsing overlapping ranges isn't even worth it.
Part 2 is just "fold overlapping pairs" though. So do it anyway.
"""

def parse_data(lines):
    bounds = []
    queries = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "-" in line:
            left, right = map(int, line.split("-"))
            bounds.append((left, right))
        else:
            queries.append(int(line))
    return bounds, queries


def reduce_bounds(bounds):
    reduced = []
    if not bounds:
        return reduced
    bounds = sorted(bounds, reverse=True)
    current_left, current_right = bounds.pop()
    while bounds:
        left, right = bounds.pop()
        if current_right < left:
            reduced.append((current_left, current_right))
            current_left = left
            current_right = right
        else:
            current_right = max(right, current_right)
    reduced.append((current_left, current_right))
    return reduced


TEST_DATA = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

test_lines = TEST_DATA.split()
bounds, queries = parse_data(test_lines)
with open("05.txt") as f:
    lines = f.readlines()
    bounds, queries = parse_data(lines)

bounds = reduce_bounds(bounds)

fresh = 0
for query in queries:
    if any(bound[0] <= query <= bound[1] for bound in bounds):
        fresh += 1
print(fresh)

total_fresh = sum(b[1] - b[0] + 1 for b in bounds)
print(total_fresh)
