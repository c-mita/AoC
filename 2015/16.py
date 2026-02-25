"""
Really simple, just test everything against the constraints provided. We're
assured that only one will match.
"""


def parse_input(filename):
    data = {}
    with open(filename) as f:
        for line in f:
            name, rest = line.strip().split(": ", 1)
            stuff = {}
            elts = rest.split(", ")
            for elt in elts:
                thing, value = elt.split(": ")
                stuff[thing] = int(value)
            n = int(name.split(" ")[1])
            data[n] = stuff
    return data


def fits_constraints(properties, constraints):
    for p, v in properties.items():
        if p in constraints and v != constraints[p]:
            return False
    return True


def fits_imprecise_constraints(properties, constraints):
    for p, v in properties.items():
        if p not in constraints:
            continue
        if p == "cats" or p == "trees":
            if v <= constraints[p]:
                return False
        elif p == "pomeranians" or p == "goldfish":
            if v >= constraints[p]:
                return False
        else:
            if v != constraints[p]:
                return False
    return True


constraints = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

data = parse_input("16.txt")
fitting = [n for n in data if fits_constraints(data[n], constraints)]
print(fitting[0])
fitting = [n for n in data if fits_imprecise_constraints(data[n], constraints)]
print(fitting[0])
