import time


TRAP = "^"

def parse_file(filename):
    with open(filename) as f:
        return [TRAP == t for t in f.read().replace("\n", "")]

def next_row(row):
    row = [False] + row + [False]
    next_row = [row[i] ^ row[i+2] for i in xrange(len(row)-2)]
    return next_row

def safe_tile_count(row, row_max):
    safe_sum = 0
    for x in xrange(row_max):
        safe_sum += len(row) - sum(row)
        row = next_row(row)
    return safe_sum

row0 = parse_file("18.txt")
st = time.time()
print safe_tile_count(row0, 40)
print time.time() - st
st = time.time()
print safe_tile_count(row0, 400000) # ~6 seconds
print time.time() - st
