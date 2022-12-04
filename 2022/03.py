def parse_input(filename):
    with open(filename) as f:
        return [l.strip() for l in f]


SYMBOLS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
PRIORITIES = {c:n+1 for (n, c) in enumerate(SYMBOLS)}

backpacks = parse_input("03_input.txt")

# Part 1
duplicates = []
for backpack in backpacks:
    # set intersection is a little heavy handed, but does the job
    l = len(backpack)
    first, second = backpack[:int(l / 2)], backpack[int(l / 2):]
    fs, ss = set(first), set(second)
    duplicates.append((fs & ss).pop())

print(sum(PRIORITIES[d] for d in duplicates))

# Part 2
group_labels = []
for a, b, c in zip(backpacks[:-2:3], backpacks[1:-1:3], backpacks[2::3]):
    a, b, c = set(a), set(b), set(c)
    group_labels.append(set.intersection(a, b, c).pop())

print(sum(PRIORITIES[l] for l in group_labels))
