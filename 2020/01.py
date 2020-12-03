def parse_input(filename):
    with open(filename) as f:
        return map(int, f.readlines())

# Part 1
entries = set(parse_input("01.txt"))
for entry in entries:
    if 2020 - entry in entries:
        print entry, 2020 - entry, entry * (2020 - entry)
        break

# Part 2
# Naive n^2 solution, but it's still quick
for entry in entries:
    target = 2020 - entry
    subset = entries - {entry}
    for e2 in subset:
        if target - e2 in subset:
            print entry, e2, target - e2, entry * e2 * (target - e2)
            break
    else:
        continue
    break
