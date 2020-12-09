def parse_file(filename):
    with open(filename) as f:
        return [int(l.strip()) for l in f]


def check_for_sum(v, seq):
    for s in seq:
        if v - s in seq:
            return True
    return False


def find_first_invalid(sequence, check_length=25):
    for n, v in enumerate(sequence[check_length:]):
        priors = sequence[n:n+check_length]
        if not check_for_sum(v, priors):
            return n, v
    raise ValueError("No invalid numbers")


def find_subsequence(sequence, target):
    for n, _ in enumerate(sequence):
        s = 0
        for m, v in enumerate(sequence[n:]):
            s += v
            if s == target:
                return sequence[n:n+m+1]
            elif s >= target:
                break
    raise ValueError("No subsequence")


sequence = parse_file("09.txt")
invalid_idx, invalid_value = find_first_invalid(sequence)
print invalid_value
subseq = find_subsequence(sequence, invalid_value)
print min(subseq) + max(subseq)
