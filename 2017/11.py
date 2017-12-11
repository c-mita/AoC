"""
Hex grid using coordinate system s.t.
nw = (-1, +1)
n  = (0, +1)
ne = (+1, 0)
se = (+1, -1)
s  = (0, -1)
sw = (-1, 0)

Axis is aligned vertically and along one of the diagonals of the hexagons
("cadinal directions are vertical (along north-south) and along ne-sw line)
"""

def parse_input(filename):
    instructions = []
    with open(filename) as f:
        for l in f:
            instructions.extend(l.strip().split(","))
    return instructions

def calc_positions(steps):
    x, y = 0, 0
    positions = [(0, 0)]
    for step in steps:
        if step == "nw": x, y = x-1, y+1
        elif step == "n": x, y = x, y+1
        elif step == "ne": x, y = x+1, y
        elif step == "se": x, y = x+1, y-1
        elif step == "s": x, y = x, y-1
        elif step == "sw": x, y = x-1, y
        else: raise ValueError("Unknown instruction %s" % step)
        positions.append((x, y))
    return positions

def calc_distance(pos):
    # imaginging our hex grid is actually a diagonal slice through a cube
    # distance is manhatten distance on cube (abs(x) + abs(y) + abs(z))
    # but our steps cover twice as much ground
    # x, y, z in cube cartesian coords, p, q is our hex grid
    # x = p, y = q, z = -p - q
    p, q = pos
    return (abs(p) + abs(q) + abs(p + q)) / 2

steps = parse_input("11_input.txt")
positions = calc_positions(steps)
print calc_distance(positions[-1])
print max((calc_distance(p) for p in positions))
