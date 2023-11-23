import itertools
import operator
from collections import namedtuple


Cart = namedtuple("Cart", ["location", "direction", "next_change"])

STRAIGHT = "straight"
LEFT = "left"
RIGHT = "right"


def apply_rotation(current, rotation):
    if rotation == STRAIGHT:
        return current
    elif rotation == LEFT:
        return (current[1], -current[0])
    elif rotation == RIGHT:
        return (-current[1], current[0])
    else:
        raise ValueError("Unknown '%s'" % rotation)


def rotation_rule():
    return itertools.cycle([LEFT, STRAIGHT, RIGHT])


def process_cart(grid, cart):
    px, py = cart.location
    dx, dy = cart.direction
    x, y = px + dx, py + dy
    if grid[y][x] == "\\":
        if dx != 0:
            new_dir = apply_rotation((dx, dy), RIGHT)
        else:
            new_dir = apply_rotation((dx, dy), LEFT)
    elif grid[y][x] == "/":
        if dx != 0:
            new_dir = apply_rotation((dx, dy), LEFT)
        else:
            new_dir = apply_rotation((dx, dy), RIGHT)
    elif grid[y][x] == "+":
        new_dir = apply_rotation((dx, dy), next(cart.next_change))
    else:
        new_dir = (dx, dy)

    return Cart((x, y), new_dir, cart.next_change)


def parse_input(filename):
    grid = []
    carts = []
    with open(filename) as f:
        for (row_idx, l) in enumerate(f):
            # skip line return
            row = []
            for (n, c) in enumerate(l[:-1]):
                if c in ["<", ">"]:
                    row.append("-")
                    carts.append(Cart((n, row_idx), (1, 0) if c == ">" else (-1, 0), rotation_rule()))
                elif c in ["v", "^"]:
                    row.append("|")
                    carts.append(Cart((n, row_idx), (0, 1) if c == "v" else (0, -1), rotation_rule()))
                else:
                    row.append(c)
            grid.append(row)
    return grid, carts


grid, carts = parse_input("13_input.txt")

crash_locations = []


while len(carts) > 1:
    carts = sorted(carts, key=lambda x: (x.location[1], x.location[0]))
    for n, cart in enumerate(carts):
        if cart is None:
            continue
        new_cart = process_cart(grid, cart)
        carts[n] = new_cart
        # check for collisions
        for k in list(range(0, n)) + list(range(n+1, len(carts))):
            if carts[k] is None:
                continue
            if carts[k].location == new_cart.location:
                carts[k] = None
                carts[n] = None
                crash_locations.append(new_cart.location)
    carts = [c for c in carts if c is not None]
print(crash_locations[0])
print(carts[0].location)
