"""
Part 1:
Consider only horizontal reflections.
Walk down the rows of a pattern and maintain two lists.
For each row (numbered 1, 2, 3, ...), consider the pairs of rows:
([1],[2])
([1,2], [4,3])
([1,2,3], ([6,5,4])
...
Until the left side reaches half way (no more rows to go on the right).
We've found a reflection when the left and right side of a pair are equal.

Repeat going backwards (but skip the mid-point row, because it was already checked).

Then check for vertical lines of reflection by rotating the inut and using the same code.

The problem statement does not state this, and leaves it somewhat ambiguous, but for our
input, it appears there will only ever be one valid line of reflection.


Part 2:
We do the same, but this time we change our list comparison function.
How it returns True iff there is exactly one difference between the left and the right.

Again, there appears to only be one valid new line of reflection.
"""


import collections


def parse_file(filename):
    patterns = [[]]
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                patterns.append([])
                continue
            patterns[-1].append(line)
    return patterns


def rotate_pattern(pattern):
    if not pattern:
        return []
    rotated = [""] * len(pattern[0])
    for line in pattern:
        for n, c in enumerate(line):
            rotated[n] += c
    return rotated


def lists_equal(left, right):
    if len(left) != len(right):
        return False
    for l, r in zip(left, right):
        if l != r:
            return False
    return True


def smudged_lists_equal(left, right):
    d = 0
    if len(right) != len(right):
        return False
    for l, r in zip(left, right):
        for lc, rc in zip(l, r):
            if lc != rc:
                d += 1
            if d > 1:
                return False
    return d == 1


def find_reflection(pattern, comparison=lists_equal):
    def find_half_reflections(pattern):
        n = 0
        left_rows = collections.deque([pattern[0]])
        right_rows = collections.deque([pattern[1]])
        left = iter(pattern[1:])
        right = iter(pattern[2:])
        try:
            while True:
                if comparison(left_rows, right_rows):
                    return len(left_rows)
                left_rows.append(next(left))
                right_rows.pop()
                right_rows.appendleft(next(right))
                right_rows.appendleft(next(right))
        except StopIteration:
            return 0
    forward = find_half_reflections(pattern)
    backward = 0
    if not forward:
        backward = find_half_reflections(list(reversed(pattern))[:-1])
        if not backward:
            return 0
        backward = len(pattern) - backward
    return forward + backward


test_data = [
    [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
    ],
    [
        "#...##..#",
        "#....#..#",
        "..##..###",
        "#####.##.",
        "#####.##.",
        "..##..###",
        "#....#..#",
    ],
]

data = parse_file("13.txt")
s = 0
for pattern in data:
    rotated = rotate_pattern(pattern)
    v = find_reflection(rotated)
    h = find_reflection(pattern)
    s += 100 * h + v
print(s)

s = 0
for pattern in data:
    rotated = rotate_pattern(pattern)
    h = find_reflection(pattern, comparison=smudged_lists_equal)
    v = find_reflection(rotated, comparison=smudged_lists_equal)
    s += 100 * h + v
print(s)
