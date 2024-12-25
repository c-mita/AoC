"""
An easy victory lap for the year, as day 25 often is.
"""


def parse_block(block):
    lines = block.split("\n")
    lock = "#" in lines[0]
    l = len(lines)
    row = [-1] * len(lines[0])
    it = range(l) if lock else range(l-1, -1, -1)

    for i in it:
        for n, s in enumerate(lines[i]):
            if s == "#":
                row[n] += 1
    return lock, tuple(row)


def parse_file(filename):
    block = ""
    locks, keys = [], []
    with open(filename) as f:
        for line in f:
            if line and line != "\n":
                block += line
            else:
                lock, pattern = parse_block(block)
                if lock:
                    locks.append(pattern)
                else:
                    keys.append(pattern)
                block = ""
        if block:
            lock, pattern = parse_block(block)
            if lock:
                locks.append(pattern)
            else:
                keys.append(pattern)
    return locks, keys


def fits(lock, key):
    for v1, v2 in zip(lock, key):
        if v1 + v2 > 5:
            return False
    return True


locks, keys = parse_file("25.txt")
s = 0
for lock in locks:
    for key in keys:
        if fits(lock, key):
            s += 1
print(s)
