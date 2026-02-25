"""
Implement Conway's Game of Life.
It's not particularly fast and there's nothing else to say.
"""


def parse_input(filename):
    space = {}
    with open(filename) as f:
        for r, line in enumerate(f):
            for c, s in enumerate(line.strip()):
                space[(r, c)] = s
    return space, r+1, c+1


def iterate_game(space, fixed=None):
    def neighbours(r, c):
        yield (r-1, c-1)
        yield (r-1, c)
        yield (r-1, c+1)
        yield (r, c-1)
        yield (r, c+1)
        yield (r+1, c-1)
        yield (r+1, c)
        yield (r+1, c+1)

    next_space = {}
    for (r, c) in space:
        if fixed and (r, c) in fixed:
            next_space[(r, c)] = "#"
            continue
        living = sum((nr, nc) in space and space[(nr, nc)] == "#" for (nr, nc) in neighbours(r, c))
        if space[(r, c)] == "#" and 2 <= living <= 3:
            alive = "#"
        elif space[(r, c)] == "." and living == 3:
            alive = "#"
        else:
            alive = "."
        next_space[(r, c)] = alive
    return next_space


initial_space, size_r, size_c = parse_input("18.txt")

space = initial_space
for _ in range(100):
    space = iterate_game(space)
print(sum(v == "#" for v in space.values()))

fixed = [(0, 0), (0, size_c-1), (size_r-1, 0), (size_r-1, size_c-1)]
space = dict(initial_space)
for f in fixed:
    space[f] = "#"

for _ in range(100):
    space = iterate_game(space, fixed=fixed)
print(sum(v == "#" for v in space.values()))
