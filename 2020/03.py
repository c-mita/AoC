def parse_file(filename):
    data = []
    with open(filename) as f:
        for line in f.readlines():
            data.append([c == "#" for c in line.strip()])
    return data


def check_slopes(terrain, right, down):
    count = 0
    r, c = down, right
    while r < len(terrain):
        row = terrain[r]
        c %= len(row)

        count += row[c]

        r += down
        c += right
    return count


terrain = parse_file("03.txt")

# Part 1
print(check_slopes(terrain, 3, 1))

#Part 2
slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
trees = [check_slopes(terrain, *slope) for slope in slopes]
print(reduce(lambda v1,v2: v1*v2, trees, 1))
