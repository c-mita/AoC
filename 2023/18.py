"""
Part 1 could be solved with a simple flood fill to identify the size of the
interior. But Part 2 demands we come up with something better.

The Shoelace formula gives us the interior space of a polygon:
 A = 1/2 * sum((Xi+1 * Yi) - (Xi * Yi+1) for (Xi,Yi) in polygon) (where Xn == X0)

But we need to consider the "boundary".

If we think about the shoelace formula as giving us the area for the polygon
where coordinates are in the "centre" of the cells they mark, we note the following:

Points on an "outer" corner (outside angle is > 180 degrees) are missing 3/4 of the cell
Points on an "inner" corner are missing 1/4 of the cell.
All other points are missing 1/2 of the cell.

Our polygon doesn't overlap, so has a winding number of 1.
Therefore, outer_corners - inner_corners = 4
So, we can treat all corners as "non-corners" (because the inners and outers
balance to 1/2 of a cell missing each) and simply add 4 additional 1/4 cells.

So the final formula is:

    A = Shoelace_Area + Perimeter / 2 + 1
"""


def parse_file(filename):
    data = []
    with open(filename) as f:
        for line in f:
            d, n, code = line.strip().split(" ")
            n = int(n)
            hexcode = code[2:-1]
            data.append(((d, n), hexcode))
    return data


def steps_to_segments(steps):
    segments = []
    sx, sy = 0, 0
    dirs = {"U":(-1, 0), "D":(1, 0), "L":(0,-1), "R":(0,1)}
    for direction, distance in steps:
        dx, dy = dirs[direction]
        tx = sx + distance * dx
        ty = sy + distance * dy
        segments.append(((sx, sy), (tx, ty)))
        sx, sy = tx, ty
    return segments


def calculate_area(segments):
    if not segments[0][0] == segments[-1][1]:
        raise ValueError("Start and end points differ")
    vertices = [segments[0][0]] + [segment[1] for segment in segments]
    shoelace_area = 0
    for v1, v2 in zip(vertices[:-1], vertices[1:]):
        x1, y1 = v1
        x2, y2 = v2
        term = x2 * y1 - x1 * y2
        shoelace_area += term
    assert shoelace_area / 2 == int(shoelace_area / 2)
    shoelace_area = int(shoelace_area / 2)
    if shoelace_area < 0: shoelace_area = -shoelace_area

    perimeter_area = 0
    for (sx, sy), (tx, ty) in segments:
        dx, dy = tx - sx, ty - sy
        d = dx if dx else dy
        if d < 0: d = -d
        perimeter_area += d
    assert perimeter_area / 2 == int(perimeter_area / 2)
    perimeter_area = int(perimeter_area / 2)

    corner_area = 1
    return shoelace_area + perimeter_area + corner_area


def hex_code_to_step(code):
    dist, direction = code[:-1], code[-1]
    if direction == "0":
        direction = "R"
    elif direction == "1":
        direction = "D"
    elif direction == "2":
        direction = "L"
    elif direction == "3":
        direction = "U"
    else:
        raise ValueError("Bad code %s" % direction)
    dist = int(dist, 16)
    return direction, dist


data = parse_file("18.txt")

segments = steps_to_segments(d[0] for d in data)
area = calculate_area(segments)
print(area)

segments = steps_to_segments(hex_code_to_step(d[1]) for d in data)
area = calculate_area(segments)
print(area)
