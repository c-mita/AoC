"""
Simple enough start; just some modular arithmetic.
Edge cases need a little care for part 2.
"""

TEST_SEQUENCE = [
        "L68",
        "L30",
        "R48",
        "L5",
        "R60",
        "L55",
        "L1",
        "L99",
        "R14",
        "L82",
]

def parse_line(line):
    sign = -1 if line[0] == "L" else 1
    return sign * int(line[1:])

test_turns = [parse_line(l) for l in TEST_SEQUENCE]
with open("01.txt") as f:
    turns = [parse_line(l.strip()) for l in f]

current = 50
zeroes = 0
for turn in turns:
    current += turn
    current %= 100
    if current == 0:
        zeroes += 1
print(zeroes)

current = 50
zeroes = 0
for turn in turns:
    complete_turns = abs(turn) // 100
    partial_turn = turn % 100
    zeroes += complete_turns
    if not partial_turn:
        continue
    p = (turn + current) % 100
    if p == 0:
        zeroes += 1
    elif current != 0 and turn > 0 and p < current:
        zeroes += 1
    elif current != 0 and turn < 0 and p > current:
        zeroes += 1
    current = p
print(zeroes)
