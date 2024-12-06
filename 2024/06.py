"""
Part 1 is simple - just run the simulation as given.

For part 2, we repeat the walk, but at every step, we add an obstacle
directly in front of us (if we haven't seen that square before) and
start a second walk, checking if that enters a loop.

~3 seconds.
"""


def parse_file(filename):
    grid = {}
    with open(filename) as f:
        for r, line in enumerate(f):
            line = line.strip()
            for c, s in enumerate(line):
                grid[(r, c)] = s
    return grid


def walk(grid, pos, step):
    visited = set()
    while True:
        visited.add(pos)
        npos = (pos[0] + step[0], pos[1] + step[1])
        if npos not in grid:
            return visited
        if grid[npos] == "#":
            step = (step[1], -step[0])
        else:
            pos = npos


def walk_with_obstacles(grid, pos, step):
    visited = set()
    loops = 0

    def next_state(state):
        pos, step = state
        npos = (pos[0] + step[0], pos[1] + step[1])
        if npos in grid and grid[npos] == "#":
            step = (step[1], -step[0])
        else:
            pos = npos
        return pos, step

    def walk_to_loop(pos, step):
        inner_visited = set()
        state = (pos, step)
        while state not in visited and state not in inner_visited:
            if state[0] not in grid:
                return False
            inner_visited.add(state)
            state = next_state(state)
        return True


    tried = set([pos])
    while True:
        npos, nstep = next_state((pos, step))
        if npos not in grid:
            return loops
        if nstep == step and npos not in tried:
            # try putting an obstacle there
            tried.add(npos)
            grid[npos] = "#"
            if walk_to_loop(pos, step):
                loops += 1
            grid[npos] = "."
        visited.add((pos, step))
        pos, step = npos, nstep


grid = parse_file("06.txt")
start = next(k for k in grid if grid[k] == "^")
visited = walk(grid, start, (-1, 0))
print(len(visited))

loops = walk_with_obstacles(grid, start, (-1, 0))
print(loops)
