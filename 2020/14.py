import re
import itertools


def parse_mask(line):
    mask = line.split(" = ")[1]
    n_max = 2**36 - 1
    to_and, to_or = n_max, 0
    x_values = []
    n = 1
    for v in reversed(mask):
        if v == "1":
            to_or += n
        elif v == "0":
            to_and -= n
        elif v == "X":
            x_values.append(n)
        n *= 2
    return to_and, to_or, x_values


def parse_write(line):
    a, v = re.findall("\d+", line)
    return int(a), int(v)


def parse_file(filename):
    blocks = []
    current_block = None
    mask = None
    with open(filename) as f:
        for l in f:
            l = l.strip()
            if "mask" in l:
                if mask is not None:
                    blocks.append((mask, current_block))
                mask = parse_mask(l)
                current_block = []
            else:
                current_block.append(parse_write(l))

    blocks.append((mask, current_block))
    return blocks


def powerset(elements):
    return itertools.chain.from_iterable(
            itertools.combinations(elements, r) for r in range(len(elements) + 1))


block_writes = parse_file("14.txt")
memory = {}
for (mask_and, mask_or, x_values), writes in block_writes:
    for address, value in writes:
        value |= mask_or
        value &= mask_and
        memory[address] = value
print sum(memory.values())


floats_masks = []
for (mask_and, mask_or, x_values), _ in block_writes:
    x_masks = list(powerset(x_values))
    floats_masks.append([sum(x_mask) for x_mask in x_masks])

memory = {}
n_max = 2**36 - 1
for ((mask_and, mask_or, _), writes), floats in zip(block_writes, floats_masks):
    for address, value in writes:
        # Xs will overwrite 1s in the address with 0s sometimes, so we must mask them out so we can use OR later
        address &= n_max ^ floats[-1]
        address |= mask_or
        for f in floats:
            a = address | f
            memory[a] = value

print sum(memory.values())
