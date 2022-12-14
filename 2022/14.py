import itertools


def parse_file(filename):
    segments = []
    with open(filename) as f:
        for line in f:
            segment = []
            sections = line.strip().split(" -> ")
            for s, t in zip(sections[:-1], sections[1:]):
                s = tuple(map(int, s.split(",")))
                t = tuple(map(int, t.split(",")))
                segment.append((s, t))
            segments.append(segment)
    return segments


def map_space(segments):
    space = set()
    for segment in segments:
        for (sx, sy), (tx, ty) in segment:
            sx, tx = min(sx, tx), max(sx, tx)
            sy, ty = min(sy, ty), max(sy, ty)
            for p in itertools.product(range(sx, tx+1), range(sy, ty+1)):
                space.add(p)
    return space


class VoidReached(Exception): pass

class SandBlocked(Exception): pass

def pour_sand(space, sand_origin, floor=None):
    space = set(space)
    if not floor:
        void = max(space, key=lambda v: v[1])[1] + 1
        floor = 0x7FFFFFFF
    else:
        void = 0x7FFFFFFFF
    def drop_grain():
        if sand_origin in space:
            raise SandBlocked
        sx, sy = sand_origin
        rest = False
        while not rest:
            if sy+1 == void:
                raise VoidReached
            if sy+1 == floor:
                rest = True
            elif (sx, sy+1) not in space:
                sx, sy = sx, sy+1
            elif (sx-1, sy+1) not in space:
                sx, sy = (sx-1, sy+1)
            elif (sx+1, sy+1) not in space:
                sx, sy = (sx+1, sy+1)
            else:
                rest = True
        return sx, sy

    n = 0
    while True:
        try:
            space.add(drop_grain())
            n += 1
        except (VoidReached, SandBlocked):
            return n


sand_origin = (500, 0)
segments = parse_file("14_input.txt")
space = map_space(segments)
grains = pour_sand(space, sand_origin)
print(grains)

# Part 2
# The problem input is actually small enough that we can just leverage the
# previous solution and simulate everything (the final pyramid is less than 200
# units tall, so we're placing fewer than 40000 grains, each one taking at most
# ~200 steps (~8 million steps).
# Somewhat unsatisfying; it's not super quick (takes >1s to run).
floor = max(space, key=lambda v:v[1])[1] + 2
peak = min(space, key=lambda v:v[1])[1]
grains = pour_sand(space, sand_origin, floor=floor)
print(grains)
