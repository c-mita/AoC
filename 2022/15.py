"""
Part 1:
    For each sensor, calculate its L1 radius and then calculate the bounds of
    the line segment that it has when it intersects the desired Y value.
    Walk these X boundary values (tracking opening and closing) to count the
    size of the union of all of them. Then simply subtract the number of
    beacons at that Y

Part 2:
    More complicated. There are probably some cleverer ways to solve this
    efficiently. But here's what I've got.
    First note that, because we're told there is exactly one point not in
    the union of our sensors, we can assume that the point we're looking
    for is "next to" several other beacons (at least four).
    This means we can filter possible candidates significantly; for each
    pair of sensors test if they are next to each other and then look at
    the points along the perimeter of one of them. For each point we perform
    the naive test and eventually we will find our solution.

    Takes about 700ms, but good enough.
    Testing all perimeters takes > 1 minute.
"""

import re


def parse_file(filename):
    sensors = []
    with open(filename) as f:
        for line in f:
            sx, sy, bx, by = map(int, re.findall("-*[0-9]+", line))
            sensors.append(((sx, sy), (bx, by)))
    return sensors


def count_at_y(sensors, y):
    x_markers = []
    for (sx, sy), (bx, by) in sensors:
        l = abs(bx - sx) + abs(by - sy)
        dy = abs(y - sy)
        if dy > l:
            # our sensor doesn't intersect the target row
            continue
        # we want to know the X bounds for the segment our sensor
        # intersects our y value.
        wx = l - dy
        lx, hx = sx - wx, sx + wx
        x_markers.append((lx, True))
        x_markers.append((hx + 1, False))
        # the +1 is to make our segments represent half-open intervals
        # so the number of things can be calculated by simple subtraction
        # also means we don't worry about the ordering between elements
        # of equal x-position in our list

    x_markers = sorted(x_markers)
    v_count = 0
    overlap_count = 0
    start_x = None
    for x, opening in x_markers:
        if overlap_count and opening:
            overlap_count += 1
        elif overlap_count == 1 and not opening:
            if start_x is None:
                raise ValueError("Bad ordering of x segments")
            overlap_count -= 1
            v_count += x - start_x
        elif overlap_count and not opening:
            overlap_count -= 1
        elif not overlap_count and opening:
            start_x = x
            overlap_count += 1
        elif not overlap_count and not opening:
            raise ValueError("Closing a segment that was never open")
        else:
            raise ValueError("Not possible")
    return v_count



def find_gap(sensors_beacons, x_bounds, y_bounds):
    min_x, max_x = x_bounds
    min_y, max_y = y_bounds

    def sensor_boundary_quadrant(sensor, dx, dy):
        (sx, sy), l = sensor
        lx = max(sx - l, min_x)
        ly = max(sy + l, min_y)
        hx = min(sx + l, max_x)
        hy = min(sy + l, max_y)
        if max_x < lx or hx < min_x:
            return
        if max_y < ly or hy < min_y:
            return
        if dx <= 0 and dy >= 0:
            for p in zip(range(lx-1, sx), range(sy, hy+1)):
                yield p
        if dx >= 0 and dy >= 0:
            for p in zip(range(sx, hx+1), range(hy+1, sy, -1)):
                yield p
        if dx >= 0 and dy <= 0:
            for p in zip(range(hx+1, sx, -1), range(sy, ly-1, -1)):
                yield p
        if dx <= 0 and dy <= 0:
            for p in zip(range(sx, lx-1, -1), range(ly-1, sy)):
                yield p

    def sensor_contains(point, sensor):
        x, y = point
        (sx, sy), d = sensor
        return abs(x - sx) + abs(y - sy) <= d

    sensors = []
    for (sx, sy), (bx, by) in sensors_beacons:
        l = abs(bx - sx) + abs(by - sy)
        sensors.append(((sx, sy), l))

    # Because there is exactly one gap, it must be next to more than one
    # scanner boundary. So we can filter our search to scanners that have
    # another not quite touching them.
    # In fact, we can filter to precisely the points along the edge
    # that's facing the neighbour.
    edge_points = []
    for i in range(len(sensors)):
        for j in range(i+1, len(sensors)):
            sensor, other = sensors[i], sensors[j]
            (sx, sy), sl = sensor
            (ox, oy), ol = other
            # check if they're adjacent (separated by a gap of 1)
            # two are adjacent if their distances don't quite touch
            # d == 1 indicates they're touching
            # d == 2 indicates a gap
            d = abs(ox - sx) + abs(oy - sy)
            if d - ol - sl == 2:
                dx = ox - sx
                dy = oy - sy
                edge_points.extend(sensor_boundary_quadrant(sensor, dx, dy))
                continue

    for p in edge_points:
        for sensor in sensors:
            if sensor_contains(p, sensor):
                break
        else:
            return p


input_file = "15_input.txt"
y_value = 2000000
sensors = parse_file(input_file)
count = count_at_y(sensors, y_value)
beacons_at_y = set(bx for (_, (bx, by)) in sensors if by == y_value)
print(count - len(beacons_at_y))

gap = find_gap(sensors, (0, 4000001), (0, 4000001))
print(gap)
print(gap[0] * 4000000 + gap[1])
