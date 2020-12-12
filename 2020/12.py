def turn_left(d, angle=90):
    x, y = d
    for n in range(angle/90):
        x, y = y, -x
    return x, y


def turn_right(d, angle=90):
    x, y = d
    for n in range(angle/90):
        x, y = -y, x
    return x, y


def parse_file(filename):
    with open(filename) as f:
        return [(l[0], int(l.strip()[1:])) for l in f]


def process_step(cmd, p, d):
    px, py = p
    dx, dy = d
    c, v = cmd
    if c == "N":
        return (px, py-v), d
    elif c == "W":
        return (px-v, py), d
    elif c == "S":
        return (px, py+v), d
    elif c == "E":
        return (px+v, py), d
    elif c == "F":
        return (px+dx*v, py+dy*v), d
    elif c == "R":
        return p, turn_right(d, v)
    elif c == "L":
        return p, turn_left(d, v)
    raise ValueError("Bad cmd %s" % cmd)


def process_step_2(cmd, p, w):
    px, py = p
    wx, wy = w
    c, v = cmd
    if c == "N":
        return p, (wx, wy-v)
    elif c == "W":
        return p, (wx-v, wy)
    elif c == "S":
        return p, (wx, wy+v)
    elif c == "E":
        return p, (wx+v, wy)
    elif c == "F":
        return (px+wx*v, py+wy*v), w
    elif c == "R":
        return p, turn_right(w, v)
    elif c == "L":
        return p, turn_left(w, v)
    raise ValueError("Bad cmd %s" % cmd)


cmds = [("F",10), ("N",3), ("F",7), ("R",90), ("F",11)]
cmds = parse_file("12.txt")
p, d = (0, 0), (1, 0)
for cmd in cmds:
    p, d = process_step(cmd, p, d)
print abs(p[0]) + abs(p[1])

p, w = (0, 0), (10, -1)
for cmd in cmds:
    p, w = process_step_2(cmd, p, w)
print abs(p[0]) + abs(p[1])
