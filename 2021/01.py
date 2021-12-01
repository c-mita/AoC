def parse_file(filename):
    with open(filename) as f:
        return [int(l) for l in f]

def count_increases(depths):
    count = 0
    for v1, v2 in zip(depths[:-1], depths[1:]):
        count += v2 > v1
    return count

def count_windowed_increases(depths):
    windows = []
    for v1, v2, v3 in zip(depths[:-2], depths[1:-1], depths[2:]):
        windows.append(v1 + v2 + v3)
    return count_increases(windows)

depths = parse_file("01_input.txt")
increases = count_increases(depths)
print(increases)

windowed_increases = count_windowed_increases(depths)
print(windowed_increases)
