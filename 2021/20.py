import itertools
import collections


"""
This problem is sneaky, The example input is nicely behaved, but the actual
problem input pulls a fast one on you.
The enhancement algorithm will turn an infinite field of "." into an
infinite field of "#", and vice versa; we must handle this case.
This isn't too complicated; we can track the expanding image normally
using dicts, but noting that the default value of the dict must "alternate"
between 0 and 1 with every enhancement step when we're in this evil algorithm
case.

Nothing clever is done for part 2, so it takes several seconds to run.
"""

def parse_file(filename):
    with open(filename) as f:
        algo = next(f).strip()
        algo = [0 if c == '.' else 1 for c in algo]
        image = collections.defaultdict(lambda: 0)
        next(f)
        for x, line in enumerate(f):
            for y, c in enumerate(line.strip()):
                image[(x, y)] = 1 if c == "#" else 0
        return algo, image


def get_key(pos, image):
    x, y = pos
    seq = itertools.product(range(x-1,x+2), range(y-1,y+2))
    b = 0
    for s in seq:
        b <<= 1
        if image[s]:
            b |= 1
    return b


def get_bounds(image):
    if not image:
        return 0, 0, 0, 0
    min_x = min(image, key=lambda k: k[0])[0]
    max_x = max(image, key=lambda k: k[0])[0]
    min_y = min(image, key=lambda k: k[1])[1]
    max_y = max(image, key=lambda k: k[1])[1]
    return min_x, max_x, min_y, max_y


def enhance(image, algo, bright=False):
    if algo[0] != 0 and algo[-1] != 0:
        raise ValueError("Image will always be infinitely bright")
    if algo[0] == 1 and image.default_factory() != 1:
        enhanced = collections.defaultdict(lambda: 1)
    else:
        enhanced = collections.defaultdict(lambda: 0)
    min_x, max_x, min_y, max_y = get_bounds(image)
    for pos in itertools.product(range(min_x-1, max_x+2), range(min_y-1, max_y+2)):
        idx = get_key(pos, image)
        enhanced[pos] = algo[idx]
    return enhanced

algo, image = parse_file("20_input.txt")

e1 = enhance(image, algo)
e2 = enhance(e1, algo)
print(sum(1 if e2[e] else 0 for e in e2))

# This isn't quick, but I also don't care
enhanced = image
for _ in range(25):
    enhanced = enhance(enhanced, algo)
    enhanced = enhance(enhanced, algo)
print(sum(1 if enhanced[e] else 0 for e in enhanced))
