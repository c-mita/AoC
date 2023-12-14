"""
Part 1 is simple enough:
We just simulate the rolling in a dict. For consistency, we wrap the entire
space in "#" blocks (this handles a couple of edge conditions).

Part 2 requires we simulate a full north-west-south-east cycle.
This complicates the code for Part 1 somewhat, but not too badly.

The number of cycles is too high, but the board state will enter a loop.
We just need to identify when this happens, determine how long the loop is
and then we can identify which board state will correspond to the desired
cycle count.

Not the fastest solution, but < 5 seconds is good enough for me.
"""


def parse_file(filename):
    space = {}
    with open(filename) as f:
        for r, line in enumerate(f):
            line = line.strip()
            for c, s in enumerate(line):
                space[(r, c)] = s
    return space


def complete_space(space):
    """Wraps the space in a boundary of "#" blocks"""
    space = dict(space)
    max_r = max(k[0] for k in space)
    max_c = max(k[1] for k in space)
    for r in range(-1, max_r + 2):
        space[(r, -1)] = "#"
        space[(r, max_c+1)] = "#"
    for c in range(-1, max_c + 2):
        space[(-1, c)] = "#"
        space[(max_r+1, c)] = "#"
    return space


def roll_north(space):
    return roll(space, (-1, 0))


def roll_south(space):
    return roll(space, (1, 0))


def roll_west(space):
    return roll(space, (0, -1))


def roll_east(space):
    return roll(space, (0, 1))


def roll(space, direction):
    max_r = max(k[0] for k in space)
    max_c = max(k[1] for k in space)
    new_space = {}
    assert (direction[0] == 0) != (direction[1] == 0)

    def place_rocks(space, start, step, count):
        x, y = start
        dx, dy = step
        while count:
            space[(x, y)] = "O"
            x += dx
            y += dy
            count -= 1

    if direction[0]:
        outer = range(-1, max_c+1)
        inner = range(-1, max_r+1) if direction[0] < 0 else range(max_r, -2, -1)
    if direction[1]:
        outer = range(-1, max_r+1)
        inner = range(-1, max_c+1) if direction[1] < 0 else range(max_c, -2, -1)

    for s1 in outer:
        edge = (0, s1) if direction[0] else (s1, 0)
        to_place = 0
        for s2 in inner:
            r, c = (s2, s1) if direction[0] else (s1, s2)
            symbol = space[(r, c)]
            if symbol == "O":
                new_space[(r, c)] = "."
                if edge is None:
                    # there may be no "." before we see a "O" block
                    edge = (s2, s1) if direction[0] else (s1, s2)
                to_place += 1
                continue
            new_space[(r, c)] = symbol
            if symbol == "." and edge is None:
                if edge is None:
                    edge = (s2, s1) if direction[0] else (s1, s2)
            elif symbol == "#" and edge is not None:
                dx, dy = -direction[0], -direction[1]
                place_rocks(new_space, edge, (dx, dy), to_place)
                edge = None
                to_place = 0
    return new_space


def cycle(space):
    space = roll_north(space)
    space = roll_west(space)
    space = roll_south(space)
    space = roll_east(space)
    return space


def run_cycles(space, cycles=1000000000):
    def space_key(space):
        return tuple(sorted(k for k in space if space[k] == "O"))

    states = {}
    key = space_key(space)
    s = space
    n = 0
    while key not in states:
        states[key] = n
        s = cycle(s)
        key = space_key(s)
        n += 1

    # we've entered a loop, but we need to know the loop length
    loop_states = {}
    loop = {}
    l = 0
    while key not in loop_states:
        loop_states[key] = l
        loop[l] = s
        s = cycle(s)
        key = space_key(s)
        l += 1

    k = cycles - n
    return loop[k % len(loop)]


def space_load(space):
    max_r = max(k[0] for k in space)
    gen = (max_r - k[0] for k in space if space[k] == "O")
    return sum(gen)


def space_to_str(space):
    rows = []
    max_r = max(k[0] for k in space)
    min_r = min(k[0] for k in space)
    max_c = max(k[1] for k in space)
    min_c = min(k[1] for k in space)

    for r in range(min_r, max_r+1):
        rows.append("".join(space[(r, c)] for c in range(min_c, max_c+1)))
    return "\n".join(rows)


data = parse_file("14.txt")
space = complete_space(data)

rolled_space = roll_north(space)
load = space_load(rolled_space)
print(load)

final_state = run_cycles(space)
print(space_load(final_state))
