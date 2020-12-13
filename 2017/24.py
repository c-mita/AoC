def parse_file(filename):
    with open(filename) as f:
        adapters = {}
        for l in f:
            v1, v2 = map(int, l.strip().split("/"))
            adapters.setdefault(v1, set()).add((v1, v2))
            adapters.setdefault(v2, set()).add((v1, v2))
        return adapters


def chains(adapters, port=0, chain=()):
    yield chain
    for a in adapters[port]:
        if a not in chain:
            p = a[0] if a[1] == port else a[1]
            for c in chains(adapters, p, chain + (a,)):
                yield c


def chain_strength(chain):
    return sum(a1 + a2 for a1, a2 in chain)


adapters = parse_file("24_input.txt")
max_strength = 0
max_length = (0, 0)
for chain in chains(adapters):
    s = chain_strength(chain)
    if s > max_strength:
        max_strength = s
    l = len(chain)
    if l > max_length[0]:
        max_length = (l, chain_strength(chain))
    elif l == max_length[0] and chain_strength(chain) > max_length[1]:
        max_length = (l, chain_strength(chain))

print max_strength
print max_length[1]
