"""
Easy problem. Just do what the problem description says we should do.
Leverage an ordered dict for part 2, avoiding list manipulation stuff.
"""


import collections


def parse_file(filename):
    with open(filename) as f:
        line = next(f)
    return line.strip().split(",")


def calc_hash(s):
    v = 0
    for c in s:
        v += ord(c)
        v *= 17
        v %= 256
    return v


def apply_operation(store, op):
    if "=" in op:
        label, value = op.split("=")
        value = int(value)
        o = "="
    else:
        label = op[:-1]
        o = op[-1]
    h = calc_hash(label)
    box = store[h]
    if o == "=":
        box[label] = value
    if o == "-" and label in box:
        del box[label]


def score_box(box):
    s = 0
    for n, (l, v) in enumerate(box.items()):
        s += (n + 1) * v
    return s


data = parse_file("15.txt")
hash_sum = sum(calc_hash(s) for s in data)
print(hash_sum)

store = [collections.OrderedDict() for n in range(256)]
for op in data:
    apply_operation(store, op)

score = 0
for n, box in enumerate(store):
    score += (n+1) * score_box(box)
print(score)
