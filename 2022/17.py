"""
For Part 1 it's enough to just simulate the falling rocks, calculating the
height after enough rocks have fallen.
Fir Part 2, we need to be more clever. We note that the pattern of the surface
we're falling onto actually enters a cycle (along with the index into our jet
pattern); with that we don't need to simulate all that much before we can
calculate how high the tower will be.
"""


def parse_file(filename):
    with open(filename) as f:
        return f.readlines()[0].strip()

FLAT = [(0,0), (0,1), (0,2), (0,3)]
PLUS = [(0,1), (1,0), (1,1,), (1,2), (2,1)]
CORNER = [(0,0), (0,1), (0,2), (1,2), (2,2)]
TALL = [(0,0), (1,0), (2,0), (3,0)]
SQUARE = [(0,0), (0,1), (1,0), (1,1)]


def falling_rocks():
    n = 0
    rocks = [FLAT, PLUS, CORNER, TALL, SQUARE]
    while True:
        rock = rocks[n]
        n += 1
        n %= len(rocks)
        yield list(rock), n


def jet_pressure(jet_code):
    n = 0
    while True:
        s = jet_code[n]
        n += 1
        n %= len(jet_code)
        yield (0, 1 if s == ">" else -1), n


def draw_space(space):
    lines = []
    row = 0
    found = True
    while found:
        found = any((row, y) in space for y in range(7))
        line = ["#" if (row, y) in space else "." for y in range(7)]
        lines.append("".join(line))
        row += 1
    return "\n".join(reversed(lines))


def simulate_rocks(rock_source, jet_source, max_rocks=2022):
    width = 7
    current_height = 0
    space = {(-1, y) for y in range(width)}
    for _ in range(max_rocks):
        rock, rn = next(rock_source)
        rock = {(x + current_height + 3, y + 2) for (x, y) in rock}
        while True:
            (jx, jy), jn = next(jet_source)
            moved_rock = {(x+jx, y+jy) for (x, y) in rock}
            hit_wall = any(y < 0 or width <= y for (x, y) in moved_rock)
            if not hit_wall and not moved_rock & space:
                rock = moved_rock
            moved_rock = {(x-1, y) for (x, y) in rock}
            if moved_rock & space:
                current_height = max(current_height, max(rock)[0] + 1)
                space |= rock
                break
            rock = moved_rock
    return current_height, space


def find_loop(rock_source, jet_source):
    width = 7
    def reduce_front(space):
        front = []
        for cy in range(width):
            x = max(x for (x,y) in space if y == cy)
            front.append((x, cy))
        return tuple((x, y) for (x, y) in front)
    def calc_front(space):
        front = reduce_front(space)
        min_x = min(front)[0]
        return tuple((x - min_x, y) for (x, y) in front)

    current_height = 0
    space = {(-1, y) for y in range(width)}
    # front_space represents space but only the surface level
    # it's very wasteful to be calculating the frontage of the entire space
    # every time we finish moving a rock, since most of the elements are
    # buried.
    front_space = set(space)
    fronts = {}
    changes = []
    n = 0
    while True:
        rock, rn = next(rock_source)
        rock = {(x + current_height + 3, y + 2) for (x, y) in rock}
        while True:
            (jx, jy), jn = next(jet_source)
            moved_rock = {(x+jx, y+jy) for (x, y) in rock}
            hit_wall = any(y < 0 or width <= y for (x, y) in moved_rock)
            if not hit_wall and not moved_rock & space:
                rock = moved_rock
            moved_rock = {(x-1, y) for (x, y) in rock}
            if moved_rock & space:
                next_height = max(current_height, max(rock)[0] + 1)
                space |= rock
                front = calc_front(front_space | rock)
                if (front, rn, jn) in fronts:
                    start_n, _ = fronts[(front, rn, jn)]
                    return start_n, n - start_n, changes
                fronts[(front, rn, jn)] = n, next_height - current_height
                changes.append(next_height - current_height)
                current_height = next_height
                front_space = set(front)
                break
            rock = moved_rock
        n += 1
    return None

TEST_JETS = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
jets = parse_file("17_input.txt")
fallen, space = simulate_rocks(falling_rocks(), jet_pressure(jets))
print(fallen)
#print(draw_space(space))

loop_start, loop_length, height_changes = find_loop(falling_rocks(), jet_pressure(jets))
target = 1000000000000
initial_height = sum(height_changes[n] for n in range(loop_start))
loop_change = sum(height_changes[n] for n in range(loop_start, loop_start + loop_length))
loops = int((target - loop_start) // loop_length)
loop_pos = (target - loop_start) % loop_length
final_change = sum(height_changes[n] for n in range(loop_start, loop_start + loop_pos))
d = initial_height + loop_change * loops + final_change
print(d)
