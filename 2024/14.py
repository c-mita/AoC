"""
A weird one...

Part 1 is easy. Just apply the velocity for t=100 and wrap to fit the grid.
Part 2...
I am not interested in writing a Christmas Tree pattern matcher.
An "entropy" based identifier might work for identifying an "unusually
low entropy" arrangement.

In the end we just look for the first time a "significant majority" of
robots have a neighbour. Other image arrangements are unlikely...
"""


import re


def parse_file(filename):
    data = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data.append(tuple(map(int, re.findall("-?\d+", line))))
    return data


def process(pos, vec, steps=1):
    px, py = pos
    vx, vy = vec
    nx = px + steps * vx
    ny = py + steps * vy
    return (nx, ny)


def closeness(positions):
    has_neighbour = 0
    for px, py in positions:
        paired = False
        paired |= (px-1, py-1) in positions
        paired |= (px-1, py) in positions
        paired |= (px-1, py+1) in positions
        paired |= (px+1, py-1) in positions
        paired |= (px+1, py) in positions
        paired |= (px+1, py+1) in positions
        paired |= (px, py-1) in positions
        paired |= (px, py+1) in positions
        if paired:
            has_neighbour += 1
    return has_neighbour / len(positions)


data = parse_file("14.txt")

final_coords = [process((r[0], r[1]), (r[2], r[3]), steps=100) for r in data]
wrapped_coords = [(px % 101, py % 103) for (px, py) in final_coords]

quadrants = [0, 0, 0, 0]
for px, py in wrapped_coords:
    if px < 50 and py < 51:
        quadrants[0] += 1
    elif px > 50 and py < 51:
        quadrants[1] += 1
    elif px < 50 and py > 51:
        quadrants[2] += 1
    elif px > 50 and py > 51:
        quadrants[3] += 1
print(quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3])

coords = [(v[0], v[1]) for v in data]
vecs = [(v[2], v[3]) for v in data]
close_ratio = 0
steps = 0
while close_ratio < 0.66:
    coords = [process(c, v) for (c, v) in zip(coords, vecs)]
    coords = [(px % 101, py % 103) for (px, py) in coords]
    close_ratio = closeness(set(coords))
    steps += 1
print(steps)
