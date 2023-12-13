"""
For part 1, we simply perform a BFS on the input, recording how many steps
we take before we run out of places to walk to.

For part 2, we perform a variation of the ray-cast test to determine if points
are in the loop (using a crude winding number calculation).

For each point on the boundary, we mark if it's moving up or down (+1/-1).
For each row, we walk the line and sum the marks as we go. If we see the same
non-zero mark twice in a row we skip it.
e.g. -1, 0, +1, 0, +1 sums to +1, not +2

This prevents us double counting:
e.g., in L-7; L and 7 both are marked "+1", but only one should count for the
ray cast, because the sums of the cells immediately to the left of L and right
of 7 should differ only by 1 (one is outside and one is inside).

This is ok because we know our path does not self-intersect.
"""


def parse_input(filename):
    grid = {}
    with open(filename) as f:
        for r, line in enumerate(f):
            for c, symbol in enumerate(line.strip()):
                if symbol != ".":
                    grid[(r, c)] = symbol
    return grid


def valid_starts(grid, start):
    r, c = start
    if (r-1, c) in grid and grid[(r-1, c)] in ["|", "7", "F"]:
        yield (r-1, c)
    if (r, c-1) in grid and grid[(r, c-1)] in ["L", "F", "-"]:
        yield (r, c-1)
    if (r, c+1) in grid and grid[(r, c+1)] in ["7", "J", "-"]:
        yield (r, c+1)
    if (r+1, c) in grid and grid[(r+1, c)] in ["|", "J", "L"]:
        yield (r+1, c)


def interpret_grid(grid):
    pipe_maze = {}
    for (r, c), symbol in grid.items():
        neighbours = {
                "|": ((r-1, c), (r+1, c)),
                "L": ((r-1, c), (r, c+1)),
                "J": ((r-1, c), (r, c-1)),
                "-": ((r, c-1), (r, c+1)),
                "7": ((r+1, c), (r, c-1)),
                "F": ((r+1, c), (r, c+1)),
        }
        if symbol == "S":
            pipe_maze[(r, c)] = tuple(v for v in valid_starts(grid, (r, c)))
        else:
            pipe_maze[(r, c)] = neighbours[symbol]
    return pipe_maze


def bfs_walk(pipe_maze, start):
    front = [start]
    seen = set()
    seen.add(start) # set(tuple) does the wrong thing
    n = -1
    while front:
        n += 1
        next_front = []
        for p in front:
            for np in pipe_maze[p]:
                if np not in seen:
                    next_front.append(np)
                    seen.add(np)
        front = next_front
    return n, seen


def boundary_walk(pipe_maze, start):
    marks = {}
    seen = set()
    pos = start
    while True:
        steps = [p for p in pipe_maze[pos] if p not in seen]
        if not steps:
            break
        step = steps[0]
        dr, dc = step[0] - pos[0], step[1] - pos[1]
        if dr != 0:
            marks[pos] = dr
            marks[step] = dr
        else:
            marks[step] = 0 # only want "-" to be marked with 0
        seen.add(step)
        pos = step
    return marks


def ray_cast_interior_count(marks):
    count = 0
    rows = max(p[0] for p in marks) + 1
    cols = max(p[1] for p in marks) + 1
    for row in range(rows):
        last_mark = 0
        mark_sum = 0
        for col in range(cols):
            pos = (row, col)
            if pos in marks:
                mark = marks[pos]
                if mark == last_mark:
                    continue
                if mark != 0:
                    last_mark = mark
                mark_sum += mark
            elif mark_sum != 0:
                count += 1
    return count


data = parse_input("10.txt")
for pos, symbol in data.items():
    if symbol == "S":
        start = pos
        break

pipe_maze = interpret_grid(data)
distance, pipes = bfs_walk(pipe_maze, start)
print(distance)

winding_marks = boundary_walk(pipe_maze, start)
contained = ray_cast_interior_count(winding_marks)
print(contained)
