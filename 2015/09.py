"""
The number of unique routes is quite small; there are only 8 locations so
the number of routes is 8! (40320).

In fact, there are fewer effective ones due to symmetry (A->B->C is the
same as C->B->A), but there's no need to handle that because the problem
is so bounded.
"""


import itertools


def parse_input(filename):
    distances = {}
    with open(filename) as f:
        for line in f:
            elts = line.strip().split(" ")
            n1, n2 = elts[0], elts[2]
            d = int(elts[-1])
            distances[(n1, n2)] = d
    return distances


def journey_distance(itinerary, distances):
    d = 0
    for n1, n2 in zip(itinerary[:-1], itinerary[1:]):
        d += distances[(n1, n2)]
    return d


data = parse_input("09.txt")
distances = dict(data)
locations = set()
for (n1, n2), d in data.items():
    distances[(n2, n1)] = d
    locations.add(n1)
    locations.add(n2)

perms = itertools.permutations(locations)
perm_distances = [journey_distance(route, distances) for route in perms]
print(min(perm_distances))
print(max(perm_distances))
