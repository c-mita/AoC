def parse_file(filename):
    with open(filename) as f:
        return [int(x) for x in f.readlines()]

def find_first_repeat(deltas):
    f = 0
    seen = set()
    idx = 0
    while f not in seen:
        seen.add(f)
        f += deltas[idx]
        idx = (idx + 1) % len(deltas)
    return f


deltas = parse_file("01_input.txt")
print sum(deltas)
print find_first_repeat(deltas)
