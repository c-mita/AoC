"""
Union-find with a priority queue for walking the edges.

Generating the O(n^2) set of edges is a little unfortunate but at least we
don't have to fully sort it by converting it to a heap

For part 1 we just track the sizes of sets given by their representative node.
For part 2 we just keep going until a set reaches the size of all nodes.
"""


import heapq


def parse_data(data):
    if type(data) == str:
        data = data.split()
    points = []
    for line in data:
        line = line.strip()
        if not line:
            continue
        points.append(tuple(map(int, line.split(","))))
    return points


def d2_distance(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    d = abs(x1 - x2)**2
    d += abs(y1 - y2)**2
    d += abs(z1 - z2)**2
    return d


def distance_mapping(points):
    distances = []
    for i in range(len(points)):
        p1 = points[i]
        for j in range(i+1, len(points)):
            p2 = points[j]
            d = d2_distance(p1, p2)
            distances.append((d, (p1, p2)))
    heapq.heapify(distances)
    return distances


def find(point, unioned, sizes=None):
    while parent := unioned.get(point, None):
        # flatten the tree a little on each walk (optional, but helps)
        if grandparent := unioned.get(parent, None):
            unioned[point] = grandparent
        point = parent
    if sizes != None and point not in sizes:
        sizes[point] = 1
    return point


def connect_pairs(points, target=1000):
    points = list(points)
    unioned = {}
    sizes = {}
    while points and target:
        target -= 1
        _distance, (p1, p2) = heapq.heappop(points)
        r1 = find(p1, unioned, sizes)
        r2 = find(p2, unioned, sizes)
        if r1 != r2:
            unioned[r1] = r2
            sizes[r2] += sizes[r1]
            del sizes[r1]
    return sizes


def connect_all(points_heap):
    pending = set()
    unioned = {}
    sizes = {}
    for _d, (p1, p2) in points_heap:
        pending.add(p1)
        pending.add(p2)
    points_heap = list(points_heap)
    while points_heap:
        _distance, (p1, p2) = heapq.heappop(points_heap)
        r1 = find(p1, unioned, sizes)
        r2 = find(p2, unioned, sizes)
        if r1 != r2:
            unioned[r1] = r2
            sizes[r2] += sizes[r1]
            del sizes[r1]
            if sizes[r2] == len(pending):
                return p1, p2
    raise ValueError("Never fully connected")


TEST_DATA = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

test_points = parse_data(TEST_DATA)
with open("08.txt") as f:
    points = parse_data(f)

distance_heap = distance_mapping(points)

circuit_sizes = connect_pairs(distance_heap, target=1000)
sizes = sorted(circuit_sizes.values())
product = 1
for s in sizes[-1:-4:-1]:
    product *= s
print(product)

final_pair = connect_all(distance_heap)
print(final_pair[0][0] * final_pair[1][0])
