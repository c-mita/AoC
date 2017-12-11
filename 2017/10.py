INPUT = "165,1,255,31,87,52,24,113,0,91,148,254,158,2,73,153"

def iterate_hash(input_list, mutation_lengths, idx=0, skip=0):
    l = list(input_list)
    length = len(l)
    for m in mutation_lengths:
        if m + idx > length:
            to_reverse = l[idx:] + l[:m - (length-idx)]
            r = to_reverse[::-1]
            l[idx:] = r[:length-idx]
            l[:m - (length-idx)] = r[length-idx:]
        else:
            to_reverse = l[idx:idx + m]
            r = to_reverse[::-1]
            l[idx:idx + m] = r
        idx += m + skip
        idx %= length
        skip += 1
    return l, idx, skip

mutated, idx, skip = iterate_hash(range(256), [int(d) for d in INPUT.split(",")])
print mutated[0] * mutated[1]

input_string = INPUT
input_bytes = [ord(c) for c in input_string] + [17, 31, 73, 47, 23]
idx, skip = 0, 0
seq = range(256)
for n in xrange(64):
    seq, idx, skip = iterate_hash(seq, input_bytes, idx, skip)

knot_hash_bytes = []
for n in xrange(16):
    block = seq[16*n:16*n+16]
    xor = 0
    for b in block:
        xor ^= b
    knot_hash_bytes.append(xor)
knot_hash = "".join(format(b, '02x') for b in knot_hash_bytes)
print knot_hash
