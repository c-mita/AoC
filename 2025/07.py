"""
For part 1 just track the front of "tachyons" in a set and count everytime
we encounter a splitter.

Part 2 is a small modification; we just need to track how many ways we could
reach a given coordinate as we walk down the grid. Whenever a tachyon would
"walk off the grid", we add the number of ways we could reach it to our total.
(Alternatively we could likely just sum up the last row, but the way I've
stored things is less amenable to that approach).
"""


def parse_data(data):
    grid = {}
    if type(data) == str:
        data = data.split("\n")
    for r, line in enumerate(data):
        for c, s in enumerate(line.strip()):
            grid[(r, c)] = s
    return grid


def run_beam(grid):
    start = [pos for pos in grid if grid[pos] == "S"][0]
    beams = {start}
    routes = {start:1}
    splits = 0
    total_routes = 0
    while beams:
        next_beams = set()
        for beam in beams:
            multiplicity = routes[beam]
            nbeam = beam[0] + 1, beam[1]
            if nbeam not in grid:
                total_routes += routes[beam]
                continue
            if grid[nbeam] == "^":
                nbeams = ((nbeam[0], nbeam[1] - 1), (nbeam[0], nbeam[1] + 1))
                splits += 1
            else:
                nbeams = (nbeam,)
            for n in nbeams:
                if n not in routes:
                    routes[n] = 0
                routes[n] += multiplicity
                next_beams.add(n)
        beams = next_beams
    return splits, total_routes


TEST_INPUT = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

test_grid = parse_data(TEST_INPUT)
with open("07.txt") as f:
    grid = parse_data(f)

splits, total_routes = run_beam(grid)
print(splits)
print(total_routes)
