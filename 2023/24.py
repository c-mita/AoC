"""
Part 1 we can solve with some simple equation solving.
Identify the intersection of all combinations of rays and count the ones
inside the "test" area.

Part 2.
Don't think about the rock we throw as "moving". Make it stationary by
subtracting its velocity from all hailstone velocities.
Then, its position will be where all the "hailstone rays" intersect.

"Guess" possible x, y velocities for the rock and filter out the ones
that don't have all rays interecting in the future. Then we look for a
z velocity and see if things work out.
"""


import itertools


def parse_file(filename):
    data = []
    with open(filename) as f:
        for line in f:
            pos, vel = line.strip().split(" @ ")
            pos = tuple(map(int, pos.split(", ")))
            vel = tuple(map(int, vel.split(", ")))
            data.append((pos, vel))
    return data


def ray_xy_intersection(r1, r2):
    s1, v1 = r1
    s2, v2 = r2

    s1x, s1y = s1
    s2x, s2y = s2
    v1x, v1y = v1
    v2x, v2y = v2

    dx = s2x - s1x
    dy = s2y - s1y
    det = v2x * v1y - v1x * v2y
    if det == 0:
        return False

    t1 = (dy * v2x - dx * v2y) / det
    t2 = (dy * v1x - dx * v1y) / det
    if t1 < 0 or t2 < 0:
        return False

    p1x, p1y = s1x + v1x * t1, s1y + v1y * t1
    return p1x, p1y


def points_at_distance(radius):
    if radius == 0:
        yield 0, 0
        return

    for x in (-radius, radius):
        for y in range(-radius, radius+1):
            yield x, y
    for y in (-radius, radius):
        for x in range(-radius+1, radius):
            yield x, y


def find_rock_velocity(stones):

    def test_xy_vec(vx, vy):
        px, py = None, None
        times = {}
        for s1, s2 in zip(stones, stones[1:] + [stones[0]]):
            s1_s, s1_v = s1
            s2_s, s2_v = s2
            s1_s, s1_v = s1_s[:-1], s1_v[:-1]
            s2_s, s2_v = s2_s[:-1], s2_v[:-1]
            s1_v = s1_v[0] - vx, s1_v[1] - vy
            s2_v = s2_v[0] - vx, s2_v[1] - vy
            # this is a hack - the xy intersection doesn't work when
            # the paths are parallel, even though there may be intersections
            if s1_v[0] and s1_v[1] and s2_v[0] / s1_v[0] == s2_v[1] / s1_v[1]:
                continue
            xy = ray_xy_intersection((s1_s, s1_v), (s2_s, s2_v))
            if not xy:
                return False
            x, y = xy
            if int(x) != x or int(y) != y:
                return False
            x, y = int(x), int(y)
            if px is None:
                px = x
            if py is None:
                py = y
            if px != x or py != y:
                return False
            if s1_v[0] == 0:
                return False
            if s2_v[0] == 0:
                return False
            t1 = (x - s1_s[0]) / s1_v[0]
            t2 = (x - s2_s[0]) / s2_v[0]
            if t1 < 0 or t2 < 0:
                return False
            if t1 != int(t1) or t2 != int(t2):
                return False
            times[s1] = int(t1)
            times[s2] = int(t2)
        return times, (int(px), int(py))

    radius = 0
    while True:
        solution = None
        for x, y in points_at_distance(radius):
            solution = test_xy_vec(x, y)
            if not solution:
                continue
            times, (px, py) = solution
            # technically incorrect because the correct z might be outside
            # these bounds and we won't ever check it again in the future...
            for z in range(-radius, radius+1):
                pz = None
                for (s_pos, s_vec), t in times.items():
                    if not t:
                        # a run of parallel lines will lead  us to writing
                        # zero for times; just skip these if they come up
                        continue
                    dz = s_vec[2] - z
                    potential_z = s_pos[2] + t * dz
                    if pz is None:
                        pz = potential_z
                    if potential_z != pz:
                        break
                else:
                    if pz is not None:
                        return (px, py, pz), (x, y, z)
        radius += 1


test_data = "24_test.txt", 7, 27
real_data = "24.txt", 200000000000000, 400000000000000
filename, lower, upper = real_data
rays = parse_file(filename)
points = []

for r1, r2 in itertools.combinations(rays, 2):
    r1 = r1[0][:-1], r1[1][:-1]
    r2 = r2[0][:-1], r2[1][:-1]
    intersection = ray_xy_intersection(r1, r2)
    if intersection:
        x, y = intersection
        if lower <= x <= upper and lower <= y <= upper:
            points.append((x, y))
print(len(points))

start, velocity = find_rock_velocity(rays)
print(sum(start))
