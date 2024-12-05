def parse_file(filename):
    left, right = [], []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            l, r = map(int, line.split("   "))
            left.append(l)
            right.append(r)
    return left, right

left, right = parse_file("01.txt")

left = sorted(left)
right = sorted(right)

# Part 1
d = 0
for l, r in zip(left, right):
    d += abs(r - l)
print(d)

# Part 2
counts = {}
for v in right:
    if v not in counts:
        counts[v] = 0
    counts[v] += 1

s = 0
for l in left:
    v = counts[l] if l in counts else 0
    s += l * v
print(s)
