def parse_file(filename):
    with open(filename) as f:
        return [tuple(map(int, l.strip().split(" "))) for l in f]


def is_safe(levels, skip=False):
    # will not handle the first two elements properly
    dec, inc = False, False
    it = iter(levels)
    prev = next(it)
    for v in it:
        d = v - prev
        a = abs(d)
        if not (1 <= a <= 3):
            if skip:
                skip = False
                continue
            return False

        if d < 0 and inc:
            if skip:
                skip = False
                continue
            return False
        if d > 0 and dec:
            if skip:
                skip = False
                continue
            return False

        inc += d > 0
        dec += d < 0
        prev = v
    return True


data = parse_file("02.txt")
safe = sum(1 if is_safe(levels) else 0 for levels in data)
print(safe)

safe = 0
# check reversed to handle the cases where the elements to remove are the
# first two (this doesn't work out properly otherwise)
for levels in data:
    if is_safe(levels, skip=True) or is_safe(reversed(levels), skip=True):
        safe += 1
print(safe)
