"""
This took me longer than I would care to admit.
Part 1 is simple; just check every pair of points.

Part 2 is more complex.
The idea is to trace out the boundary lines of the enclosed shape and then,
for every edge of a rectangle described by two points, check for intersection
with this boundary.

This is non-trivial. We first check for the winding number of the path.
The example given has a negative number so we make sure our input matches.
This means that, when we're walking along the path, the outside edge of the shape
is always to our left (given our cells are always inside). So we can descibe every
edge of the boundary precisely (the top-left corner of the first cell is (0,0).

Draw every rectangle line through the "middle" of the cells describing it and
perform intersection checks. We can use binary search to clip the potentially
interesting lines by ordering vertical lines according to x coordinates
and horizontal lines by y coordinate. (x, y) is (column, row), unlike my usual
convention of (row, column).

This fails if the path is a tight zig-zag (it assumes an "outside edge" is
actually touching an outside cell). This is probably reparable though (if
two outside edges overlap in a range, they can both be ignored within
that range).

~1.5 seconds, so not ideal, but not terrible.
"""


import bisect


def parse_data(data):
    if type(data) == str:
        data = data.split("\n")
    points = []
    for line in data:
        line = line.strip()
        if not line:
            continue
        x, y = map(int, line.split(","))
        points.append((x, y))
    return points


def find_greatest_pair(points):
    largest = 0
    for i in range(len(points)):
        x1, y1 = points[i]
        for j in  range(i+1, len(points)):
            x2, y2 = points[j]
            # the +1 because a difference of "0" still covers a 1x1 cell
            d = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if d > largest:
                largest = d
    return largest


def connect_pairs(points):
    edges = []
    first = points[-1]
    for second in points:
        edges.append((first, second))
        first = second
    return edges


def calc_direction(edge):
    (e1x, e1y), (e2x, e2y) = edge
    dx = 1 if e1x < e2x else -1 if e1x > e2x else 0
    dy = 1 if e1y < e2y else -1 if e1y > e2y else 0
    if (dx == 0) == (dy == 0):
        return ValueError(f"Bad direction for '{edge}'")
    return dx, dy


def orient_turn(e1, e2):
    d1x, d1y = calc_direction(e1)
    d2x, d2y = calc_direction(e2)
    if d1x == -d2y and d1y == d2x:
        return 1
    elif d1x == d2y and d1y == -d2x:
        return -1
    raise ValueError("Non-rotation for '%s'", [e1, e2])


def orient_curve(edges):
    first = edges[-1]
    t = 0
    for second in edges:
        t += orient_turn(first, second)
        first = second
    return -1 if t < 0 else 1


def orient_points(points):
    m = len(points)
    orientation = {}
    for idx in range(0, m):
        prev = points[(idx - 1) % m]
        ahead = points[(idx + 1) % m]
        current = points[idx]
        turn = orient_turn((prev, current), (current, ahead))
        orientation[current] = turn
    return orientation


def bounding_edges(edges, orientations):
    # assume a negative winding number
    # that is, the true bounds of the enclosed shape are to our left
    # when walking around the curve
    y_edges = []
    x_edges = []
    for p1, p2 in edges:
        # -1 means turning right (clockwise); include the current cell in the boundary
        current_turn = orientations[p1]
        next_turn = orientations[p2]
        p1x, p1y = p1
        p2x, p2y = p2
        if (p1x == p2x) == (p1y == p2y):
            raise ValueError()
        if p1x < p2x:
            y_line = p1y
            start_x = p1x if current_turn < 0 else p1x + 1
            end_x = p2x + 1 if next_turn < 0 else p2x
            y_edges.append(((start_x, y_line), (end_x, y_line)))
        elif p1x > p2x:
            y_line = p1y + 1
            start_x = p2x if next_turn < 0 else p2x + 1
            end_x = p1x + 1 if current_turn < 0 else p1x
            y_edges.append(((start_x, y_line), (end_x, y_line)))
        elif p1y < p2y:
            x_line = p1x + 1
            start_y = p1y if current_turn < 0 else p1y + 1
            end_y = p2y + 1 if next_turn < 0 else p2y
            x_edges.append(((x_line, start_y), (x_line, end_y)))
        elif p1y > p2y:
            x_line = p1x
            start_y = p2y if next_turn < 0 else p2y + 1
            end_y = p1y + 1 if current_turn < 0 else p1y
            x_edges.append(((x_line, start_y), (x_line, end_y)))
        else:
            raise ValueError()
    x_edges = sorted(x_edges, key=lambda v:v[0][0])
    y_edges = sorted(y_edges, key=lambda v:v[0][1])
    return x_edges, y_edges


def edges_in_range(x1, x2, edges, key):
    start_idx = bisect.bisect_right(edges, x1, key=key)
    end_idx = bisect.bisect_left(edges, x2, key=key)
    for idx in range(start_idx, end_idx):
        yield edges[idx]


def bounded_pairs(points):
    edges = connect_pairs(points)
    # ensure a negative winding number (the same as the test input)
    # this means our boundary is always to the left when walking the loop
    if orient_curve(edges) > 0:
        points = list(reversed(points))
        edges = connect_pairs
    oriented_points = orient_points(points)
    vertical_lines, horizontal_lines = bounding_edges(edges, oriented_points)

    def pairs():
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                yield points[i], points[j]

    def lines_in_range(lines, lower, upper, axis):
        start_idx = bisect.bisect_right(lines, lower, key=lambda v:v[0][axis])
        end_idx = bisect.bisect_left(lines, upper, key=lambda v:v[0][axis])
        for idx in range(start_idx, end_idx):
            yield lines[idx]

    def line_intersects(query, lines, fixed_axis, varied_axis):
        fixed = query[0][fixed_axis]
        q1, q2 = query[0][varied_axis], query[1][varied_axis]
        if q2 < q1:
            q2 = q1
        for line in lines_in_range(lines, q1, q2, varied_axis):
            line_start, line_end = line[0][fixed_axis], line[1][fixed_axis]
            if line_start == line_end:
                raise ValueError("OOPS")
            if line_start <= fixed < line_end:
                return True
        return False

    for p1, p2 in pairs():
        p1x, p1y = p1
        p2x, p2y = p2
        if p1x > p2x:
            p1x, p2x = p2x, p1x
        if p1y > p2y:
            p1y, p2y = p2y, p1y

        # run our rectangle boundary lines through the middle of cells
        # our path boundary runs on the border of cells, so this avoids
        # some edge cases when testing for intersects.
        p1x += 0.5
        p1y += 0.5
        p2x += 0.5
        p2y += 0.5

        h1_line = ((p1x, p1y), (p2x, p1y))
        h2_line = ((p1x, p2y), (p2x, p2y))
        v1_line = ((p1x, p1y), (p1x, p2y))
        v2_line = ((p2x, p1y), (p2x, p2y))
        intersects = False
        if (not (line_intersects(h1_line, vertical_lines, 1, 0)
                or line_intersects(h2_line, vertical_lines, 1, 0)
                or line_intersects(v1_line, horizontal_lines, 0, 1)
                or line_intersects(v2_line, horizontal_lines, 0, 1))):
            yield p1, p2


def find_greatest_bounded_pair(points):
    largest = 0
    for p1, p2 in bounded_pairs(points):
        x1, y1 = p1
        x2, y2 = p2
        d = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        if d > largest:
            largest = d
    return largest


TEST_INPUT = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

test_points = parse_data(TEST_INPUT)
with open("09.txt") as f:
    points = parse_data(f)

biggest = find_greatest_pair(points)
print(biggest)

bounded_biggest = find_greatest_bounded_pair(points)
print(bounded_biggest)
