"""
For Part 2, we track the number of times each symbol appears and each relevant pairs.
"""



import collections

def parse_input(filename):
    mappings = {}
    with open(filename) as f:
        lines = f.readlines()
    chain = lines[0].strip()
    for line in lines[2:]:
        k, v = line.strip().split(" -> ")
        mappings[k] = v
    return chain, mappings


def process_input(chain, mappings):
    # count how many times each symbol occurs, and each pair
    pairs = collections.defaultdict(int)
    symbols = collections.defaultdict(int)
    for v1, v2 in zip(chain[:-1], chain[1:]):
        k = v1 + v2
        if k in mappings:
            pairs[k] += 1
        symbols[v1] += 1
    symbols[chain[-1]] += 1
    return symbols, pairs


def apply_insertions_naive(chain, mappings):
    result = []
    for v1, v2 in zip(chain[:-1], chain[1:]):
        result.append(v1)
        k = v1 + v2
        if k in mappings:
            result.append(mappings[k])
    result.append(chain[-1])
    return "".join(result)


def apply_insertions(symbols, pairs, mappings):
    # every mapping replaces a pair with two new ones and adds one symbol
    new_pairs = collections.defaultdict(int)
    new_symbols = collections.defaultdict(int)
    new_symbols.update(symbols)
    for k, count in pairs.items():
        c1, c2 = k[0], k[1]
        ins = mappings[k]
        new_pairs[c1 + ins] += count
        new_pairs[ins + c2] += count
        new_symbols[ins] += count
    return new_symbols, new_pairs


initial_chain, mappings = parse_input("14_input.txt")
chain = initial_chain
for n in range(10):
    chain = apply_insertions_naive(chain, mappings)

symbols = collections.defaultdict(int)
for c in chain:
    symbols[c] += 1
most_common = max(symbols[c] for c in symbols)
least_common = min(symbols[c] for c in symbols)
print(most_common - least_common)

initial_symbols, initial_pairs = process_input(initial_chain, mappings)

symbols, pairs = initial_symbols, initial_pairs
for n in range(40):
    symbols, pairs = apply_insertions(symbols, pairs, mappings)
most_common = max(symbols[c] for c in symbols)
least_common = min(symbols[c] for c in symbols)
print(most_common - least_common)
