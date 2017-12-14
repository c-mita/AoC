INPUT = "jzgqcdpd"

def knothash_bytes(to_hash):
    # Copied from 10.py
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

    input_bytes = [ord(c) for c in to_hash] + [17, 31, 73, 47, 23]
    idx, skip = 0, 0
    seq = range(256)
    for n in xrange(64):
        seq, idx, skip = iterate_hash(seq, input_bytes, idx, skip)

    knot_hash_bytes = []
    for n in xrange(16):
        block = seq[16*n:16*n+16]
        xor = 0
        for b in block: xor ^= b
        knot_hash_bytes.append(xor)
    return knot_hash_bytes


def find_regions(rows_bin):
    def neighbours(r, c):
        n = [(r-1, c), (r, c-1), (r, c+1), (r+1, c)]
        return [(r, c) for (r, c) in n if 0 <= r < len(rows_bin) and 0 <= c < len(rows_bin[0])]
    marked_grid = [[0] * len(r) for r in rows_bin]

    regions = 0
    for r_idx in xrange(len(rows_bin)):
        for c_idx in xrange(len(rows_bin[r_idx])):
            if marked_grid[r_idx][c_idx] or rows_bin[r_idx][c_idx] == '0': continue
            regions += 1
            # Depth-first marking - mark all reachable points that haven't been marked already
            marked_grid[r_idx][c_idx] = regions
            to_check = [(r, c) for (r, c) in neighbours(r_idx, c_idx) if rows_bin[r][c] == '1']
            while to_check:
                r, c = to_check.pop(0)
                if marked_grid[r][c]: continue
                marked_grid[r][c] = regions
                to_check.extend([(rn, cn) for (rn, cn) in neighbours(r, c) if rows_bin[rn][cn] == '1'])
    return regions, marked_grid


hashes = [knothash_bytes("%s-%d" % (INPUT, n)) for n in xrange(128)]

rows_bin = ["".join(format(b, '08b') for b in h) for h in hashes]
print sum(b.count('1') for b in rows_bin)

regions, markings = find_regions(rows_bin)
print regions
