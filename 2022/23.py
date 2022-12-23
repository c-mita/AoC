import collections


def parse_file(filename):
    elves = set()
    with open(filename) as f:
        for r, line in enumerate(f):
            for c, v in enumerate(line.strip()):
                if v == "#":
                    elves.add((r, c))
    return elves


def instructions_gen():
    first = ["N", "S", "W", "E"]
    second = ["S", "W", "E", "N"]
    third = ["W", "E", "N", "S"]
    fourth = ["E", "N", "S", "W"]
    while True:
        yield first
        yield second
        yield third
        yield fourth


def step_elves(elves, instructions):
    proposals = collections.defaultdict(list)
    new_elves = set()
    for elf in elves:
        ex, ey = elf
        neighbours = [
                (ex-1, ey-1), (ex-1, ey), (ex-1, ey+1),
                (ex, ey-1), (ex, ey+1),
                (ex+1, ey-1), (ex+1, ey), (ex+1, ey+1),
        ]
        if not any(n in elves for n in neighbours):
            new_elves.add(elf)
            continue
        north = [(ex-1, ey-1), (ex-1, ey), (ex-1, ey+1)]
        south = [(ex+1, ey-1), (ex+1, ey), (ex+1, ey+1)]
        west = [(ex-1, ey-1), (ex, ey-1), (ex+1, ey-1)]
        east = [(ex-1, ey+1), (ex, ey+1), (ex+1, ey+1)]
        for instruction in instructions:
            if instruction == "N" and not any(n in elves for n in north):
                proposals[(ex-1, ey)].append(elf)
                break
            elif instruction == "S" and not any(n in elves for n in south):
                proposals[(ex+1, ey)].append(elf)
                break
            elif instruction == "W" and not any(n in elves for n in west):
                proposals[(ex, ey-1)].append(elf)
                break
            elif instruction == "E" and not any(n in elves for n in east):
                proposals[(ex, ey+1)].append(elf)
                break
        else:
            new_elves.add(elf)

    moved = False
    for pos, elves in proposals.items():
        if len(elves) == 1:
            new_elves.add(pos)
            moved = True
        else:
            for elf in elves:
                new_elves.add(elf)
    return new_elves, moved


def move_elves(elves, limit=10):
    ig = instructions_gen()
    for _ in range(limit):
        elves, _ = step_elves(elves, next(ig))
    return elves


def move_until_fixed(elves):
    ig = instructions_gen()
    moved = True
    n = 0
    while moved:
        n += 1
        elves, moved = step_elves(elves, next(ig))
    return elves, n


elves_start = parse_file("23_input.txt")
elves_10 = move_elves(elves_start)
min_x = min(elves_10, key = lambda v:v[0])[0]
max_x = max(elves_10, key = lambda v:v[0])[0]
min_y = min(elves_10, key = lambda v:v[1])[1]
max_y = max(elves_10, key = lambda v:v[1])[1]
wx, wy = max_x - min_x, max_y - min_y
wx, wy = wx + 1, wy + 1 # make them half-open intervals
print(wx * wy - len(elves_10))

final_elves, n = move_until_fixed(elves_start)
print(n)
