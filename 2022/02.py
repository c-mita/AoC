
SCORE_MAP = {
        ("A", "X") : 4,
        ("A", "Y") : 8,
        ("A", "Z") : 3,
        ("B", "X") : 1,
        ("B", "Y") : 5,
        ("B", "Z") : 9,
        ("C", "X") : 7,
        ("C", "Y") : 2,
        ("C", "Z") : 6,
}

# Map the part 2 input semantics to the part 1 input semantics
TO_SELECT_MAP = {
    ("A", "X") : ("A", "Z"),
    ("A", "Y") : ("A", "X"),
    ("A", "Z") : ("A", "Y"),
    ("B", "X") : ("B", "X"),
    ("B", "Y") : ("B", "Y"),
    ("B", "Z") : ("B", "Z"),
    ("C", "X") : ("C", "Y"),
    ("C", "Y") : ("C", "Z"),
    ("C", "Z") : ("C", "X"),
}

def parse_file(filename):
    result = []
    with open(filename) as f:
        for line in f:
            if not line:
                continue
            (first, second) = line.strip().split(" ")
            result.append((first, second))
    return result


# Part 1
turns = parse_file("02_input.txt")
game = (SCORE_MAP[turn] for turn in turns)
print(sum(game))

# Part 2
new_turns = (TO_SELECT_MAP[turn] for turn in turns)
print(sum(SCORE_MAP[turn] for turn in new_turns))
