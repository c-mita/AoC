"""
Part 1 is part 1 - do the thing

For part 2, walk through each buyer's values and map each difference sequence
to the value at that end of the first instance of that sequence.
Then just add that value to a map of sequence to score for that sequence.
"""


def parse_file(filename):
    with open(filename) as f:
        return list(map(int, (line.strip() for line in f)))


def produce_values(seed):
    value = seed
    while True:
        v = value
        yield v
        v = v ^ (v << 6)  # v * 64
        v &= 0xFFFFFF  # v % 16777216
        v = v ^ (v >> 5)  # v // 32
        v &= 0xFFFFFF
        v = v ^ (v << 11)  # v * 2048
        v &= 0xFFFFFF
        value = v


def sequence_map(values):
    seqeuences = {}
    if len(values) < 5:
        raise ValueError("Not enough")
    it = iter(values)
    v1 = next(it)
    v2 = next(it)
    v3 = next(it)
    v4 = next(it)
    v5 = next(it)
    d1 = v2 - v1
    d2 = v3 - v2
    d3 = v4 - v3
    d4 = v5 - v4
    v = v5
    for nv in it:
        d1 = d2
        d2 = d3
        d3 = d4
        d4 = nv - v
        seq = (d1, d2, d3, d4)
        if seq not in seqeuences:
            seqeuences[seq] = nv
        v = nv
    return seqeuences



data = parse_file("22.txt")
test_data = [1, 2, 3, 2024]

s = 0
secrets = []
for seed in data:
    values = []
    gen = produce_values(seed)
    values = [next(gen) for _ in range(2001)]
    secrets.append(values)
    s += values[-1]
print(s)


buyers = []
for values in secrets:
    prices = [v % 10 for v in values]
    buyers.append(prices)

tuple_scores = {}
for prices in buyers:
    sequences = sequence_map(prices)
    for seq in sequences:
        if seq not in tuple_scores:
            tuple_scores[seq] = 0
        tuple_scores[seq] += sequences[seq]
print(max(tuple_scores.values()))
