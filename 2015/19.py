"""
Just do the transformations for part 1.

For part 2 we can actually do a simple calculation.
First note that the transformations in the input have a pattern.

Let "X" represent any atom (potentially different ones) that is not
"Rb", "Ar", or "Y"

Then the transformation patterns are:

X -> X X
X -> X Rb X Ar
X -> X Rb X Y X Ar
X -> X Rb X Y X Y X Ar

This is clearer if you replace "Rb", "Y", "Ar" with "( , )".

We can then walk the transformations backwards, noting that each one
always reduces the number of "tokens" (atoms).

A reversal of X->XX decreases the number of tokens by 1.
A reversal of X->(X) decreases the number of tokens by 3
A reversal of X->(X,X) decreases the number of tokens by 5
A reversal of X->(X,X,X) decreases the number of tokens by 7

So we can start with assuming the number of required steps to reduce
the number of tokens down to "1" is simply "len(tokens) - 1".

But a "(" token means two fewer steps (since it eliminates itself,
its closing partner, and an element encapsulated by it).

Similarly, every "," can be paired with an extra "X", so every ","
means two fewer reductions are required.

So if there is a solution, it must have the following number of steps:
N = n_tokens - 1 - 2 * n_Rn - 2 * n_Y
"""


def parse_input(filename):
    with open(filename) as f:
        mappings = []
        for line in f:
            line = line.strip()
            if not line:
                break
            src, target = line.split(" => ")
            mappings.append((src, target))
        molecule = next(f).strip()
    return mappings, molecule


def find_all(s, pattern):
    for i in range(len(s) - len(pattern) + 1):
        for j in range(len(pattern)):
            if s[i + j] != pattern[j]:
                break
        else:
            yield i


def apply(transform, s):
    target, change = transform
    for idx in find_all(s, target):
        yield s[:idx] + change + s[idx + len(target):]


def tokenize(data):
    if not data:
        return
    token = data[0]
    i = 1
    while i < len(data):
        v = data[i]
        if v.isupper():
            yield token
            token = ""
        token += v
        i += 1
    yield token


transforms, medicine_molecule = parse_input("19.txt")

options = set()
for transform in transforms:
    for s in apply(transform, medicine_molecule):
        options.add(s)
print(len(options))

tokens = list(tokenize(medicine_molecule))

steps = len(tokens) - 1
steps -= 2 * sum(1 for t in tokens if t == "Rn")
steps -= 2 * sum(1 for t in tokens if t == "Y")
print(steps)
