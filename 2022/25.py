def parse_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f]


def snafu_to_ten(snafu):
    n = 0
    for s in snafu:
        n *= 5
        if s == "-":
            n -= 1
        elif s == "=":
            n -= 2
        else:
            n += int(s)
    return n


def ten_to_snafu(n):
    t = []
    mapping = {-2:"=", -1:"-", 0:"0", 1:"1", 2:"2"}
    while n:
        r = n % 5
        if r <= 2:
            t.append(mapping[r])
        else:
            # r > 2 means we need to subtract here and add a bigger thing
            # for the next symbol (remember, we're building the string
            # up backwards.
            n += r
            t.append(mapping[r - 5])
        n //= 5
    # we added in the wrong order
    return "".join(reversed(t))

snafu_numbers = parse_file("25_input.txt")
s = sum(snafu_to_ten(snafu) for snafu in snafu_numbers)
snafu_s = ten_to_snafu(s)
print(snafu_s)
