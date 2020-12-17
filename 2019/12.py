import re
import fractions


def parse_line(line):
    return map(int, re.findall("[-]*\d+", line))


def parse_file(filename):
    with open(filename) as f:
        return [parse_line(l) for l in f]


def lcm(v1, *args):
    if len(args) == 1:
        v2 = args[0]
        return abs(v1 * v2) / fractions.gcd(v1, v2)
    else:
        return lcm(v1, lcm(*args))


def apply_gravity(positions):
    v_deltas = []
    # this compares an element to itself, but it doesn't matter
    for px, py, pz in positions:
        dx, dy, dz = 0, 0, 0
        for ox, oy, oz in positions:
            if px > ox: dx -= 1
            if px < ox: dx += 1
            if py > oy: dy -= 1
            if py < oy: dy += 1
            if pz > oz: dz -= 1
            if pz < oz: dz += 1
        v_deltas.append((dx, dy, dz))
    return v_deltas


def apply_velocities(positions, velocities):
    new_positions = []
    for (px, py, pz), (vx, vy, vz) in zip(positions, velocities):
        new_positions.append((px+vx, py+vy, pz+vz))
    return new_positions


def cycle(positions, velocities):
    v_deltas = apply_gravity(positions)
    velocities = apply_velocities(velocities, v_deltas)
    positions = apply_velocities(positions, velocities)
    return positions, velocities


def calc_energy(position, velocity):
    px, py, pz = map(abs, position)
    vx, vy, vz = map(abs, velocity)
    return (px+py+pz) * (vx+vy+vz)


def find_axis_cycles(positions, velocities):
    pvx, pvy, pvz = {}, {}, {}
    n = 0
    x_loop, y_loop, z_loop = None, None, None
    while (not x_loop) or (not y_loop) or (not z_loop):
        px, py, pz = tuple(tuple((k[n]) for k in positions) for n in range(3))
        vx, vy, vz = tuple(tuple((k[n]) for k in velocities) for n in range(3))
        if (px, vx) in pvx:
            x_loop = pvx[(px, vx)], n - pvx[(px, vx)]
        if (py, vy) in pvy:
            y_loop = pvy[(py, vy)], n - pvy[(py, vy)]
        if (pz, vz) in pvz:
            z_loop = pvz[(pz, vz)], n - pvz[(pz, vz)]
        pvx[(px, vx)] = n
        pvy[(py, vy)] = n
        pvz[(pz, vz)] = n
        positions, velocities = cycle(positions, velocities)
        n += 1
    return x_loop, y_loop, z_loop


initial_positions = parse_file("12.txt")
#initial_positions = [(-1, 0, 2), (2, -10, -7), (4, -8, 8), (3, 5, -1)]
initial_velocities = [(0, 0, 0)] * len(initial_positions)

positions = initial_positions
velocities = initial_velocities
for n in range(1000):
    positions, velocities = cycle(positions, velocities)

print sum(calc_energy(p, v) for (p, v) in zip(positions, velocities))

xl, yl, zl = find_axis_cycles(initial_positions, initial_velocities)
print xl, yl, zl
cycle_length = lcm(xl[1], yl[1], zl[1])
# I've not really convinced myself that this is _always_ sufficient, but it is for our input
# we don't do anything to account for the fact we might not always _start_ in the loop
print cycle_length
