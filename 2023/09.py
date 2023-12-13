"""
Nothing clever; just do what the problem description says you should do.
For part 2, we just reverse our input sequences.
"""


def parse_file(filename):
    with open(filename) as f:
        return [list(map(int, l.strip().split(" "))) for l in f]


def identify_next(sequence):
    if not any(sequence):
        return 0
    differences = [r - l for (l, r) in zip(sequence[:-1], sequence[1:])]
    diff = identify_next(differences)
    return sequence[-1] + diff

data = parse_file("09.txt")

result = sum(identify_next(seq) for seq in data)
print(result)

reverse_result = sum(identify_next(list(reversed(seq))) for seq in data)
print(reverse_result)
