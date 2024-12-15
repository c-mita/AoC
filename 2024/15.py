"""
Probably the first "time consuming" problem of the year.

Part 1 we solve by writing a recursive function to see if the current
object can be "moved". If it can, we move it.

Part 2 is more difficult.
It's not too difficult to write the test to see if an object is moveable
using a similar recursive function, handling the two symbol boxes.
If it does, a second recursive function blindly moves the boxes.

Not a tidy solution, but getting things neatly in order is more effort than
I feel like spending now.
"""


def parse_file(filename):

    def parse_map(f):
        grid = {}
        line = next(f).strip()
        r = 0
        while line:
            for c, s in enumerate(line):
                grid[(r, c)] = s
            line = next(f).strip()
            r += 1
        return grid

    def parse_steps(f):
        steps = []
        try:
            line = next(f).strip()
            while line:
                steps.extend(line)
                line = next(f).strip()
        except StopIteration:
            pass
        return steps

    with open(filename) as f:
        grid = parse_map(f)
        steps = parse_steps(f)
    return grid, steps


def display_grid(grid):
    max_r = max(k[0] for k in grid)
    max_c = max(k[1] for k in grid)
    lines = []
    for r in range(max_r + 1):
        line = ""
        for c in range(max_c + 1):
            line += grid[(r, c)]
        lines.append(line)
    return "\n".join(lines)


def run_steps(grid, steps):
    delta = {"^":(-1, 0), "<": (0, -1), "v": (1, 0), ">": (0, 1)}
    grid = dict(grid)
    def step_object(position, step):
        # we check if the thing can move in the given direction
        # and return the position after trying
        thing = grid[position]
        px, py = position
        dx, dy = delta[step]
        tx, ty = px + dx, py + dy
        target = (tx, ty)

        if thing == "#":
            return False
        if thing == ".":
            return True
        if thing == "O" or thing == "@":
            moved = step_object(target, step)
            if not moved:
                return False if thing == "O" else position
            grid[target] = thing
            grid[position] = "."
            return True if thing == "O" else target

    robot = [k for k in grid if grid[k] == "@"][0]
    for step in steps:
        robot = step_object(robot, step)
    return grid


def expand_grid(grid):
    expanded = {}
    for (r, c), v in grid.items():
        if v == ".":
            v1, v2 = ".", "."
        elif v == "#":
            v1, v2 = "#", "#"
        elif v == "@":
            v1, v2 = "@", "."
        elif v == "O":
            v1, v2 = "[", "]"
        else:
            raise ValueError("Bad value %s" % v)
        expanded[(r, 2*c)] = v1
        expanded[(r, 2*c+1)] = v2
    return expanded


def run_steps_exapanded(grid):
    delta = {"^":(-1, 0), "<": (0, -1), "v": (1, 0), ">": (0, 1)}
    grid = dict(grid)

    def box_neighbours(position, step):
        dx, dy = delta[step]
        px, py = position
        v = grid[position]
        if v == "[" and dy == 0:
            yield px + dx, py
            yield px + dx, py + 1
        elif v == "]" and dy == 0:
            yield px + dx, py - 1
            yield px + dx, py
        elif v == "[" and dy == -1:
            yield px, py + dy
        elif v == "]" and dy == -1:
            yield px, py + dy - 1
        elif v == "[" and dy == 1:
            yield px, py + dy + 1
        elif v == "]" and dy == 1:
            yield px, py + dy

    def can_move_object(position, step):
        px, py = position
        dx, dy = delta[step]
        tx, ty = px + dx, py + dy
        target = tx, ty
        thing = grid[position]

        if thing == "@":
            return can_move_object(target, step)
        elif thing == "#":
            return False
        elif thing == ".":
            return True
        elif thing == "[" or thing == "]":
            moveable = True
            for to_test in box_neighbours(position, step):
                moveable = moveable and can_move_object(to_test, step)
            return moveable
        else:
            raise ValueError("Bad value '%s'" % blocker)

    def move_object(position, step):
        px, py = position
        dx, dy = delta[step]
        tx, ty = px + dx, py + dy
        target = tx, ty
        thing = grid[position]
        blocker = grid[target]

        if blocker == "#":
            raise ValueError("Cannot move when blocked")

        if dy and blocker != ".":
            move_object(target, step)
            grid[target] = thing
            grid[position] = "."
            return target

        if blocker == "[" or blocker == "]":
            other_target = tx, (ty + 1) if blocker == "[" else (ty - 1)
            move_object(target, step)
            grid[target] = thing
            grid[position] = "."
            move_object(other_target, step)
            grid[other_target] = "."
            grid[position] = "."
            return target
        elif blocker == ".":
            grid[target] = thing
            grid[position] = "."
            return target
        else:
            return position
        return target

    def step_robot(position, step):
        if grid[position] != "@":
            raise ValueError("NOT THE ROBOT")

    robot = [k for k in grid if grid[k] == "@"][0]
    for step in steps:
        if can_move_object(robot, step):
            robot = move_object(robot, step)
    return grid

grid, steps = parse_file("15.txt")

final_grid = run_steps(grid, steps)
score = 0
for k, v in final_grid.items():
    if v == "O":
        score += k[0] * 100 + k[1]
print(score)

expanded = expand_grid(grid)
final_grid = run_steps_exapanded(expanded)
score = 0
for k, v in final_grid.items():
    if v == "[":
        score += k[0] * 100 + k[1]
print(score)
