"""
Just walk through every permutation of the list of people (treating the list
as a ring buffer) and calculate the "happiness" score for each.
For part 1, 8! is just not a big number.
For part 2, 9! is also not a huge number, and this solves the problem quickly enough.

<2 seconds in total is not terrible.
"""


import itertools


def parse_input(filename):
    data = {}
    with open(filename) as f:
        for line in f:
            elts = line.strip().strip(".").split(" ")
            subj, gain, score, obj = elts[0], elts[2], int(elts[3]), elts[-1]
            if gain == "lose":
                score = -score
            data[(subj, obj)] = score
    return data


def score_arrangement(people, relations):
    score = 0
    pairs = itertools.chain(zip(people[:-1], people[1:]), [(people[0], people[-1])])
    for p1, p2 in pairs:
        score += relations[(p1, p2)]
        score += relations[(p2, p1)]
    return score


relationships = parse_input("13.txt")
people = list(set(k[0] for k in relationships))

scores = (score_arrangement(p, relationships) for p in itertools.permutations(people))
print(max(scores))

for p in people:
    relationships[("me", p)] = 0
    relationships[(p, "me")] = 0
people.append("me")

scores = (score_arrangement(p, relationships) for p in itertools.permutations(people))
print(max(scores))
