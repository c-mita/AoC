import re
from collections import namedtuple

claim = namedtuple("claim", ["id", "lmargin", "tmargin", "width", "height"])


def parse_input(lines):
    return [claim._make(map(int, re.findall("\d+", s))) for s in lines]


def claim_indices(claim, xlength):
    x_start = claim.lmargin
    x_stop = x_start + claim.width
    y_start = claim.tmargin
    y_stop = y_start + claim.height
    one_d_indices = [y * xlength + x for y in range(y_start, y_stop) for x in range(x_start, x_stop)]
    return one_d_indices


def draw_claims(claims, total_x, total_y):
    fabric = [0] * (total_x * total_y)
    for claim in claims:
        for idx in claim_indices(claim, total_x):
            fabric[idx] += 1
    return fabric


def find_isolated_claims(claims, fabric, width):
    isolated_claims = []
    for claim in claims:
        indices = claim_indices(claim, width)
        coverage = (fabric[i] for i in indices)
        if all(v == 1 for v in coverage):
            isolated_claims.append(claim)
    return isolated_claims



with open("03_input.txt") as f:
    claims = parse_input(f.readlines())

fabric = draw_claims(claims, 1000, 1000)
print(len([v for v in fabric if v > 1]))
print(find_isolated_claims(claims, fabric, 1000))
