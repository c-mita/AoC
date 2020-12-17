def generate_numbers(symbols, min_s=None):
    """Generate numbers where digits are monotonically increasing"""
    if min_s is None:
        min_s = symbols[0][0]
    to_use = [v for v in symbols[0] if min_s <= v]
    if len(symbols) == 1:
        for s in to_use:
            yield s
    else:
        p10 = len(symbols) - 1
        for s in to_use:
            for v in generate_numbers(symbols[1:], s):
                yield s * 10**p10 + v


def split_digits(n):
    while n > 0:
        yield n % 10
        n /= 10


def is_valid_1(n, minimum, maximum):
    if not (minimum <= n <= maximum):
        return False
    digits = list(reversed(list(split_digits(n))))
    found_same = False
    for c1, c2 in zip(digits[:-1], digits[1:]):
        if c1 > c2:
            return False
        if c1 == c2:
            found_same = True
    return found_same


def is_valid_2(n, minimum, maximum):
    if not is_valid_1(n, minimum, maximum):
        return False
    digits = list(split_digits(n))
    for v in range(1, 10):
        if len([d for d in digits if d == v]) == 2:
            return True
    return False


MIN_V = 246540
MAX_V = 787419

symbols = [[2, 3, 4, 5, 6, 7]] + [list(range(1, 10))] * 5
print sum(1 for v in generate_numbers(symbols) if is_valid_1(v, MIN_V, MAX_V))
print sum(1 for v in generate_numbers(symbols) if is_valid_2(v, MIN_V, MAX_V))
