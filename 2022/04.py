import re

def parse_input(filename):
    def parse_line(line):
        ax, ay, bx, by = map(int,re.split("-|,", line))
        return (ax, ay), (bx, by)
    with open(filename) as f:
        return [parse_line(line.strip()) for line in f]


def fully_contains(first, second):
    (ax, ay), (bx, by) = first, second
    # if the ranges start or stop at the same place, then one contains the other
    if ax == bx or ay == by:
        return True
    lx = ax < bx
    ly = ay < by
    return lx != ly


def overlap(first, second):
    (ax, ay), (bx, by) = first, second
    values = [(ax, 0), (ay, 0), (bx, 1), (by, 1)]
    sorted_values = sorted(values)
    # check if the first two values have different sources
    # or if the middle two have the same value
    return sorted_values[0][1] != sorted_values[1][1] \
            or sorted_values[1][0] == sorted_values[2][0]


assignments = parse_input("04_input.txt")
print(sum(1 if fully_contains(*assignment) else 0 for assignment in assignments))
print(sum(1 if overlap(*assignment) else 0 for assignment in assignments))
