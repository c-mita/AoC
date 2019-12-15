import math

test = [
        (0,1),(0,4),
        (2,0),(2,1),(2,2),(2,3),(2,4),
        (3,4),
        (4,3),(4,4),
        ]

def parse_input(file_name):
    output = []
    with open(file_name) as f:
        for (n, line) in enumerate(f):
            for (m, c) in enumerate(line):
                if c == '#':
                    output.append((n, m))
    return output

asteroids = test
asteroids = parse_input("10_input.txt")

# Part 1
scores = []
for base in asteroids:
    angles = set()
    for ast in asteroids:
        if base == ast:
            continue
        dy, dx = ast[0] - base[0], ast[1] - base[1]
        angle = math.atan2(dy, dx)
        angles.add(angle)
    scores.append((base, len(angles)))

best = max(scores, key=lambda x: x[1])
base = best[0]

print best


# Part 2
# Convert every other to polar form from POV of base (reversing angle)
# angle==0 will correspond to "up" due to swapped "x and y" in our input
# shuffle angle from [-pi, pi) range to [0, 2pi) range
# sort by angle and then distance
others = [(ax, ay) for (ax, ay) in asteroids if (ax, ay) != base]
targets = []
for ax, ay in others:
    dx, dy = base[0] - ax, base[1] - ay
    angle = math.atan2(dy, dx)
    dist2 = dx*dx + dy*dy
    angle = -angle # reverse direction to account for clockwise sweep

    if angle < 0:
        angle = 2 * math.pi + angle
    targets.append(((ax, ay), (dist2, angle)))

def comp(v1, v2):
    d1, a1 = v1[1][0], v1[1][1]
    d2, a2 = v2[1][0], v2[1][1]
    if a1 < a2:
        return -1
    elif a2 < a1:
        return 1
    else:
        if d1 == d2:
            return 0
        elif d1 < d2:
            return -1
        else:
            return 1

targets = sorted(targets, cmp=comp)

# yield asteroids for each new angle
# repeats until all asteroids returned
def vaporizer(asteroids):
    while asteroids:
        remaining = []
        prev_angle = -9999999
        for ((ax, ay), (dist, angle)) in asteroids:
            if angle == prev_angle:
                remaining.append(((ax, ay), (dist, angle)))
            else:
                prev_angle = angle
                yield ((ax, ay), (dist, angle))
        asteroids = remaining

vaped = [v for v in vaporizer(targets)]
v = vaped[199]
vx, vy = v[0][0], v[0][1]
print v
print vy * 100 + vx
