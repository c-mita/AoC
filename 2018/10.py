import re

def parse_input(filename):
    x_pos, y_pos, x_vel, y_vel = [], [], [], []
    with open(filename) as f:
        for line in f.readlines():
            px, py, vx, vy = map(int, re.findall("-*\d+", line))
            x_pos.append(px)
            y_pos.append(py)
            x_vel.append(vx)
            y_vel.append(vy)
        #numbers = [map(int, re.findall("-*\d+", line)) for line in f.readlines()]
    return x_pos, y_pos, x_vel, y_vel


def calc_bounding_box(x_pos, y_pos):
    x_min, x_max = min(x_pos), max(x_pos)
    y_min, y_max = min(y_pos), max(y_pos)
    return (x_min, y_min), (x_max, y_max)


def progress_state(x_pos, y_pos, x_vel, y_vel):
    for i in xrange(len(x_pos)):
        x_pos[i] += x_vel[i]
        y_pos[i] += y_vel[i]


def regress_state(x_pos, y_pos, x_vel, y_vel):
    for i in xrange(len(x_pos)):
        x_pos[i] -= x_vel[i]
        y_pos[i] -= y_vel[i]


def string_state(x_pos, y_pos):
    (x_min, y_min), (x_max, y_max) = calc_bounding_box(x_pos, y_pos)
    grid = [[" "] * (x_max - x_min + 1) for y in xrange(y_min, y_max + 1)]
    for (x, y) in zip(x_pos, y_pos):
        grid[y - y_min][x - x_min] = '#'
    return "\n".join("".join(row) for row in grid)


test_xp = [9, 7, 3, 6, 2, -6, 1, 1, -3, 7, -2, -4, 10, 5, 4, 8, 15, 1, 8, 3, 0, -2, 5, 1, -2, 3, 5, -6, 5, 14, -3]
test_yp = [1, 0, -2, 10, -4, 10, 8, 7, 11, 6, 3, 3, -3, 11, 7, -2, 0, 6, 9, 3, 5, 2, -2, 4, 7, 6, 0, 0, 9, 7, 6]
test_xv = [0, -1, -1, -2, 2, 2, 1, 1, 1,-1, 1, 2, -1, 1, 0, 0, -2, 1, 0, -1, 0, 2, 1, 2, 2, -1, 1, 2, 1, -2, 2]
test_yv = [2, 0, 1, -1, 2, -2, -1, 0, -2, -1, 0, 0, 1, -2, -1, 1, 0, 0, -1, 1, -1, 0, 2, 1, -2, -1, 0, 0, -2, 0, -1]

x_pos, y_pos, x_vel, y_vel = parse_input("10_input.txt")
#x_pos, y_pos, x_vel, y_vel = test_xp, test_yp, test_xv, test_yv

prev_area = 0x7FFFFFFFFFFFFFFF
area = 0x7FFFFFFFFFFFFFFE
count = 0
while area < prev_area:
    progress_state(x_pos, y_pos, x_vel, y_vel)
    (x_min, y_min), (x_max, y_max) = calc_bounding_box(x_pos, y_pos)
    prev_area = area
    area = (x_max - x_min + 1) * (y_max - y_min + 1)
    count += 1

regress_state(x_pos, y_pos, x_vel, y_vel)
print string_state(x_pos, y_pos)
print count - 1
