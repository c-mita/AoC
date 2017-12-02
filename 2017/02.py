# Part 1: Sum of "max_value - min_value" of each row
# Part 2: Each row has exactly one divisible pair - sum the unique division for all rows


def parse_input(filename):
    rows = []
    with open(filename) as f:
        for l in f:
            rows.append(map(int, l.split()))
    return rows

def row_max_diff(row):
    return max(row) - min(row)

def checksum(rows):
    return sum((row_max_diff(r) for r in rows))

def divisible_pair(row):
    for (i, v1) in enumerate(row[:-1]):
        for v2 in row[i+1:]:
            if (v1 / v2) * v2 == v1:
                return (v1, v2)
            if (v2 / v1) * v1 == v2:
                return (v2, v1)

def division_sums(rows):
    return sum(v1/v2 for (v1, v2) in (divisible_pair(r) for r in rows))

rows = parse_input("02_input.txt")
print checksum(rows)
print division_sums(rows)
