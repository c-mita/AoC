"""
For part 1 we just do a depth-first walk of the grid from each "0"
and simply count how many "9"s we reach.

The same thing would work for part 2, we just don't track the
"visited" nodes, but we can score more CompSci nerd points by viewing
this with a more "dynamic" lens.

We create a grid representing the "number of ways to reach a 9 from here".
Every "9" value has a count of 1.
Then every "8" value has a count equal to the sum of all neighbouring 9s.
Repeat until we've reached everywhere we can, and then read the counts for
our "0" cells.

Time ~0.02 seconds
"""


def parse_file(filename):
    grid = {}
    with open(filename) as f:
        for r, line in enumerate(f):
            for c, d in enumerate(line.strip()):
                grid[(r, c)] = int(d)
    return grid


def neighbours(point, grid):
    def it(point):
        r, c = point
        yield (r-1, c)
        yield (r+1, c)
        yield (r, c-1)
        yield (r, c+1)
    yield from (p for p in it(point) if p in grid)


def forward_walk(start, grid):
    score = 0
    stack = [start]
    seen = set(stack)
    while stack:
        p = stack.pop()
        if grid[p] == 9:
            score += 1
        for n in neighbours(p, grid):
            if grid[n] != grid[p] + 1:
                continue
            if n in seen:
                continue
            seen.add(n)
            stack.append(n)
    return score


def reverse_walk_counts(grid):
    counts = {k:1 if grid[k] == 9 else 0 for k in grid}
    current = [k for k in grid if grid[k] == 8]
    while current:
        next_wave = []
        for k in current:
            s = 0
            for n in neighbours(k, grid):
                if grid[k] == grid[n] + 1:
                    next_wave.append(n)
                elif grid[k] == grid[n] - 1:
                    s += counts[n]
            counts[k] = s
        current = next_wave
    return counts


grid = parse_file("10.txt")
heads = [k for k in grid if grid[k] == 0]

s = 0
for head in heads:
    s += forward_walk(head, grid)
print(s)

ways_to_peaks = reverse_walk_counts(grid)
print(sum(ways_to_peaks[k] for k in ways_to_peaks if grid[k] == 0))
