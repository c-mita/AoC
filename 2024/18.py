"""
Part 1 is just a simple BFS to give the shortest path.

Part 2 offers a couple of options.
The simplest is simply to run the BFS over the expanding input
until we fail. We can use a binary search to reduce the number
of searches substantially.

An alternative would be to run through the "falling bytes" linearly
and rerun the BFS whenever a new blocker is added that is on the
current "best path". O(n*m) in the worst case?
"""


def parse_file(filename):
    with open(filename) as f:
        return [tuple(map(int, line.strip().split(","))) for line in f]


def bfs(start, target, bounds, blockers):
    (lx, ly), (ux, uy) = bounds

    def neighbours(point):
        x, y = point
        for nx, ny in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
            if (lx <= nx <= ux) and (ly <= ny <= uy) and ((nx, ny) not in blockers):
                yield nx, ny

    current = [start]
    visited = set(current)
    d = 0
    while current:
        front = []
        for node in current:
            if node == target:
                return d
            for p in neighbours(node):
                if p in visited:
                    continue
                visited.add(p)
                front.append(p)
        d += 1
        current = front
    return -1


def find_first_failure(data):
    low, high = 0, len(data)
    start = (0, 0)
    target = (70, 70)
    bounds = ((0, 0), (70, 70))
    while low < high:
        mid = (low + high) // 2
        result = bfs(start, target, bounds, set(data[:mid]))
        if result == -1:
            high = mid
        else:
            low = mid + 1
    # the search fails with data[:low]
    # the final value of data[:low] is data[low-1]
    # so that is the index we return
    return low - 1


data = parse_file("18.txt")

shortest = bfs((0, 0), (70, 70), ((0, 0), (70, 70)), set(data[:1024]))
print(shortest)

first_bad_idx = find_first_failure(data)
print(",".join(map(str, data[first_bad_idx])))
