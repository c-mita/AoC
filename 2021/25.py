import enum

"""
Just simulate the buggers.
It's not super fast or clever, but it does get the job done within a
a couple of seconds.
"""


class Direction(enum.Enum):
    east = 1
    south = 2

def parse_file(filename):
    cucumbers = {}
    with open(filename) as f:
        r = 0
        for r, line in enumerate(f):
            c = 0
            for c, v in enumerate(line.strip()):
                if v == ">":
                    cucumbers[(r, c)] = Direction.east
                elif v == "v":
                    cucumbers[(r, c)] = Direction.south
        max_r = r
        max_c = c
    return cucumbers, max_r, max_c


def stringify_sea_floor(cucumbers, max_r, max_c):
    rows = []
    for r in range(max_r + 1):
        rows.append(
                "".join(
                    "." if (r, c) not in cucumbers
                    else ">" if cucumbers[(r, c)] == Direction.east
                    else "v" for c in range(max_c+1))
        )
    return "\n".join(rows)


def move_cucumbers(cucumbers, max_r, max_c):
    east = {p:d for (p, d) in cucumbers.items() if d == Direction.east}
    south = {p:d for (p, d) in cucumbers.items() if d == Direction.south}
    def step_cucumbers(cucumbers):
        east, south = cucumbers
        moved_east, moved_south = {}, {}
        moved = False
        for (r, c), d in east.items():
            nc = (c + 1) % (max_c + 1)
            if (r, nc) not in east and (r, nc) not in south:
                moved_east[(r, nc)] = d
                moved = True
            else:
                moved_east[(r, c)] = d

        for (r, c), d in south.items():
            nr = (r + 1) % (max_r + 1)
            if (nr, c) not in moved_east and (nr, c) not in south:
                moved_south[(nr, c)] = d
                moved = True
            else:
                moved_south[(r, c)] = d
        return (moved_east, moved_south), moved

    n = 0
    in_motion = True
    moving = east, south
    while in_motion:
        moving, in_motion = step_cucumbers(moving)
        n += 1
    return n, {**moving[0], **moving[1]}

cucumbers, max_r, max_c = parse_file("25_input.txt")

n, moved = move_cucumbers(cucumbers, max_r, max_c)
print(n)
