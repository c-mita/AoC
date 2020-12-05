def parse_input(filename):
    with open(filename) as f:
        for l in f:
            yield [c == "B" or c == "R" for c in l.strip()]


def find_seq_value(sequence):
    n = 2**len(sequence)
    v = 0
    for s in sequence:
        n /= 2
        if s:
            v += n
    return v


def find_id(seq):
    r, c = find_seq_value(seq[:-3]), find_seq_value(seq[-3:])
    return r * 8 + c


# Part 1
records = list(parse_input("05.txt"))
seats = [find_id(s) for s in records]
max_id = max(seats)
print max_id

# Part 2
all_seats = [0] * (max_id + 1)
for s in seats:
    all_seats[s] = 1

# The first zeros don't count (we're looking for the first 1, 0, 1 pattern)
for n, v in enumerate(all_seats):
    if v: break
    all_seats[n] = 1
print all_seats.index(0)
