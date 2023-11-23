def checksum(ids):
    twos, threes = (0, 0)
    for id in ids:
        counts = {}
        for c in id:
            v = counts.setdefault(c, 0)
            counts[c] = v + 1
        if 2 in counts.values(): twos += 1
        if 3 in counts.values(): threes += 1
    return twos * threes


def id_diff(s1, s2):
    delta = 0
    common = []
    for (c1, c2) in zip(s1, s2):
        if c1 != c2: delta += 1
        else: common.append(c1)
    return delta, "".join(common)


def find_closest_match(ids):
    i = 0
    for i in range(len(ids) - 1):
        s1 = ids[i]
        for s2 in ids[i:]:
            delta, common = id_diff(s1, s2)
            if delta == 1:
                return common


with open("02_input.txt") as f:
    ids = f.readlines()

print(checksum(ids))
print(find_closest_match(ids))
