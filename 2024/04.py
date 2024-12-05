def parse_file(filename):
    data = {}
    with open(filename) as f:
        for r, line in enumerate(f):
            line = line.strip()
            for c, symbol in enumerate(line):
                data[(r, c)] = symbol
    return data


def xmas_patterns(coord):
    r, c = coord
    yield ((r, c-1), (r, c-2), (r, c-3))
    yield ((r-1, c-1), (r-2, c-2), (r-3, c-3))
    yield ((r-1, c), (r-2, c), (r-3, c))
    yield ((r-1, c+1), (r-2, c+2), (r-3, c+3))
    yield ((r, c+1), (r, c+2), (r, c+3))
    yield ((r+1, c+1), (r+2, c+2), (r+3, c+3))
    yield ((r+1, c), (r+2, c), (r+3, c))
    yield ((r+1, c-1), (r+2, c-2), (r+3, c-3))


def cross_patterns(coord):
    r, c = coord
    yield ((r-1, c-1), (r+1, c+1))
    yield ((r+1, c+1), (r-1, c-1))
    yield ((r-1, c+1), (r+1, c-1))
    yield ((r+1, c-1), (r-1, c+1))


data = parse_file("04.txt")

count = 0
for cell in data:
    if data[cell] == "X":
        for pattern in xmas_patterns(cell):
            for c, s in zip(pattern, "MAS"):
                if c not in data or data[c] != s:
                    break
            else:
                count += 1
print(count)

count = 0
for cell in data:
    if data[cell] == "A":
        matches = 0
        for pattern in cross_patterns(cell):
            for c, s in zip(pattern, "MS"):
                if c not in data or data[c] != s:
                    break
            else:
                matches += 1
        if matches == 2:
            count += 1
print(count)
