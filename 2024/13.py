"""
Solve a pair of simultaneous equations.

We just use Cramer's rule to solve since it's pretty easy
for the case of two equations with two unknowns.
"""


import re


def parse_file(filename):
    data = []
    with open(filename) as f:
        try:
            while True:
                a_line = next(f)
                b_line = next(f)
                p_line = next(f)
                a = tuple(map(int, re.findall("[0-9]+", a_line)))
                b = tuple(map(int, re.findall("[0-9]+", b_line)))
                p = tuple(map(int, re.findall("[0-9]+", p_line)))
                data.append((a, b, p))
                next(f)
        except StopIteration:
            return data


def solve_pattern(axy, bxy, pxy):
    ax, ay = axy
    bx, by = bxy
    px, py = pxy
    det = ax*by - bx*ay
    det_a = px*by - bx*py
    det_b = ax*py - px*ay

    if det == 0:
        return 0, 0
    a = det_a // det
    if a * det != det_a:
        return 0, 0
    b = det_b // det
    if b * det != det_b:
        return 0, 0
    return a, b


data = parse_file("13.txt")
s = 0
for axy, bxy, pxy in data:
    a, b = solve_pattern(axy, bxy, pxy)
    if a < 0 or b < 0:
        continue
    s += 3 * a + b
print(s)

s = 0
for axy, bxy, pxy in data:
    px, py = pxy
    px += 10000000000000
    py += 10000000000000
    a, b = solve_pattern(axy, bxy, (px, py))
    if a < 0 or b < 0:
        continue
    s += 3 * a + b
print(s)
