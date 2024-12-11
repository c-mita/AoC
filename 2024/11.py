"""
A problem where the input is simple enough that we don't need to parse it.

Part 1 is simple enough that the "naive" approach of using an arary would work.
But despite the fact that the problem statement says the numbers are stored in
a strict straight line, we don't actually care about their order, just how many
of each stone there are. So we can easily use a dict of value->number
(i.e. a counter).

Part 2 is trivial in this way.
"""


import collections


def digit_length(v):
    n = 0
    while v:
        n += 1
        v //= 10
    return n


def step_process(counts):
    new_counts = collections.Counter()
    for v, n in counts.items():
        d = digit_length(v)
        if v == 0:
            new_counts[v + 1] += n
        elif d % 2 == 0:
            h = d // 2
            new_counts[v % 10**h] += n
            new_counts[v // 10**h] += n
        else:
            new_counts[v * 2024] += n
    return new_counts


input_data = [890, 0, 1, 935698, 68001, 3441397, 7221, 27]

data = collections.Counter(input_data)
for _ in range(25):
    data = step_process(data)

s = 0
for v, n in data.items():
    s += n
print(s)

# another 50 steps to total 75
for _ in range(50):
    data = step_process(data)

s = 0
for v, n in data.items():
    s += n
print(s)
