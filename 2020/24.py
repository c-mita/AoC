import re
import collections



def parse_file(filename):
    with open(filename) as f:
        return [re.findall("se|sw|ne|nw|e|w", l) for l in f]

"""
(y, x)

(0,0)   (0,1)   (0,2)
    (1,0)   (1,1)   (1,2)
(2,0)   (2,1)   (2,2)
"""

def follow_step(idx, cmd):
    x, y = idx
    if cmd == "w":
        return x-1, y
    elif cmd == "e":
        return x+1, y
    v, h = cmd
    if y % 2 == 1 and h == "e":
        x += 1
    elif y % 2 == 0 and h == "w":
        x -= 1
    y = (y + 1) if v == "s" else (y - 1)
    return x, y


def follow_steps(commands, start=(0, 0)):
    pos = start
    for cmd in commands:
        pos = follow_step(pos, cmd)
    return pos


def neighbours(pos):
    x, y = pos
    n = [(x-1, y), (x+1, y)]
    if y % 2 == 0:
        n += [(x-1, y-1), (x, y-1), (x-1, y+1), (x, y+1)]
    else:
        n += [(x, y-1), (x+1, y-1), (x, y+1), (x+1, y+1)]
    return n


def cycle(black_tiles):
    front = collections.defaultdict(int)
    for t in black_tiles:
        for n in neighbours(t):
            front[n] += 1
    next_black = set()
    for t in front:
        if t in black_tiles:
            if 0 < front[t] <= 2:
                next_black.add(t)
        else:
            if front[t] == 2:
                next_black.add(t)
    return next_black



directions = parse_file("24.txt")
tile_indexes = [follow_steps(d) for d in directions]
tiles = collections.defaultdict(bool)
for t in tile_indexes:
    tiles[t] ^= True
black_0 = {t for t in tiles if tiles[t]}
print len(black_0)

black = black_0
for n in range(100):
    black = cycle(black)
print len(black)
