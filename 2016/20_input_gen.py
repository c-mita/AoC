import random

def generate_pairs(n, upper):
    pairs = []
    while n:
        r_start = random.randint(0, upper)
        r_len = random.randint(0, upper - r_start)
        r_stop = random.randint(r_start, r_start + r_len)
        pairs.append((r_start, r_stop))
        n -= 1
    return pairs

upper = 0xffffffff
pairs = generate_pairs(1000, upper)
pairs.append((0, random.randint(0, upper//3)))

filename = "20_test.txt"
with open(filename, "w") as f:
    for r_start, r_stop in pairs:
        f.write("%d-%d\n" % (r_start, r_stop))

print "Written %s ranges" % len(pairs)
