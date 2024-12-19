"""
A simply depth-first walk of the solution possibilities.

Part 2 requires tracking the number of solutions from an index, so we
need to complete the walk instead of ending it early which would be
possible for part 1, but the full walk allows us to solve both parts
in one go.
"""


def parse_file(filename):
    to_build = []
    with open(filename) as f:
        patterns = next(f).strip().split(", ")
        skip = next(f)
        to_build = [line.strip() for line in f]
    return patterns, to_build


def count_solutions(target, patterns):
    solved = {}
    def walk_possibilities(idx=0):
        if idx in solved:
            return solved[idx]
        if idx == len(target):
            solved[idx] = 1
            return solved[idx]
        solved[idx] = 0
        matches = False
        for pattern in patterns:
            t_idx = idx + len(pattern)
            if pattern == target[idx:t_idx]:
                solutions = walk_possibilities(t_idx)
                if solutions:
                    solved[idx] += solutions
        return solved[idx]

    walk_possibilities()
    return solved[0]


patterns, to_make = parse_file("19.txt")

solvable = 0
solutions = 0
for target in to_make:
    count = count_solutions(target, patterns)
    if count:
        solvable += 1
    solutions += count
print(solvable)
print(solutions)
