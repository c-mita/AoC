import re
from math import sqrt

def parse_input(filename):
    def parse_line(line):
        s = [m[1:-1].strip().split(",") for m in re.findall("<.*?>", line)]
        return tuple((int(x), int(y), int(z)) for x, y, z in (m for m in s))
    with open(filename) as f:
        return [parse_line(l) for l in f]


particles = parse_input("20_input.txt")

"""
Part 1:
v = at + v0
s = 0.5at**2 + v0t + s0
Position is dominated by the acceleration term in the asymptotic case
So we initially we just need to consider the acceleration
"""

min_accel, min_particle = 0xFFFFFFFF, -1
for (i, (s, v, a)) in enumerate(particles):
    accel = sum(abs(a) for a in a)
    if accel == min_accel:
        # two particles have equal acceleration
        v_current = (v[0], v[1], v[2])
        v_min = particles[min_particle][1]
        # should check for equal initial velocity too
        # would have to factor in initial distance and direction of motion
        if sum(abs(v) for v in v_current) < sum(abs(v) for v in v_min):
            min_particle = i
    elif accel < min_accel:
        min_accel, min_particle = accel, i
print min_accel, min_particle

"""
Part 2:
Particles collide if: 0 = 0.5*a_diff*t**2 + v0_diff*t + s0_diff has real solutions for t
i.e. sqrt(v0**2 - 2*a*s0) is real

Discrete timesteps actually make the equation
0 = 0.5*a*t*(t+1) = v0*t + s0
0 = 0.5*a*t**2 + t*(0.5a + v0) + s0

A particle that has collided once may not collide again.
"""

def solve_quadratic(a, b, c):
    if a == 0:
        if b == 0:
            return None, None
        return (float(-c) / float(b),) * 2
    d = b**2 - 4*a*c
    if d < 0:
        return None, None
    return (-b + sqrt(d)) / float(2*a), (-b - sqrt(d)) / float(2*a)



TEST = [((-6, 0, 0), (3, 0, 0), (0, 0, 0)),
        ((-4, 0, 0), (2, 0, 0), (0, 0, 0)),
        ((-2, 0, 0), (1, 0, 0), (0, 0, 0)),
        ((3, 0, 0), (-1, 0, 0), (0, 0, 0))]

collisions = {}
collision_times = {}
c = 0
for (i, p1) in enumerate(particles):
    s1, v1, a1 = p1
    for (j, p2) in enumerate(particles[i+1:]):
        s2, v2, a2 = p2
        sd = [s2c - s1c for (s1c, s2c) in zip(s1, s2)]
        vd = [v2c - v1c for (v1c, v2c) in zip(v1, v2)]
        ad = [a2c - a1c for (a1c, a2c) in zip(a1, a2)]
        # solve for any axis
        tc0, tc1 = None, None
        for (s, v, a) in zip(sd, vd, ad):
            t0, t1 = solve_quadratic(0.5*a, 0.5*a + v, s)
            if (t0, t1) != (None, None):
                tc0, tc1 = t0, t1
                break
        if tc0 is None and tc1 is None: continue
        # take the two times and check if they satisify the other axes
        # if not just set it to negative and we'll ignore it later
        for (s, v, a) in zip(sd, vd, ad):
            if 0 != 0.5*a*tc0**2 + tc0*(0.5*a + v) + s: tc0 = -1
            if 0 != 0.5*a*tc1**2 + tc1*(0.5*a + v) + s: tc1 = -1
        if tc0 < 0 and tc1 < 0: continue
        elif tc0 < 0: t = tc1
        elif tc1 < 0: t = tc0
        else: t = min(tc0, tc1)
        collision_times.setdefault(t, []).append((i, i + j + 1))

collided = set()
for t in sorted(collision_times.keys()):
    cp = collision_times[t]
    new_collisions = [(p0, p1) for (p0, p1) in cp if p0 not in collided and p1 not in collided]
    collided.update([p for pair in new_collisions for p in pair])
print "Collisions: %d" % len(collided)
print "Remaining: %d" % (len(particles) - len(collided))
