import re


REV = "r"
CUT = "c"
INC = "i"


def parse_line(line):
    if "new stack" in line:
        return (REV, None)
    elif "increment" in line:
        return (INC, int(re.findall("\d+", line)[-1]))
    elif "cut" in line:
        return (CUT, int(re.findall("-*\d+", line)[-1]))
    raise ValueError("Bad line '%s'" % line)


def parse_file(filename):
    with open(filename) as f:
        return [parse_line(l) for l in f]


"""
We can view our operations as the following linear transformations modulo N
New Deck = Mirror
Cut n = Translate by n
Inc n = Scale by n
"""
def process_transforms(commands):
    """
    Reduce the transforms to the form f(x) = p*x + d
    Returns p, d
    """
    s = 1
    p = 1
    for cmd, v in commands:
        if cmd == REV:
            s = -s - 1
            p *= -1
        elif cmd == CUT:
            s = s - v
        elif cmd == INC:
            s = s * v
            p *= v
    return p, s - 1 * p


"""
i1 = i0 * p + d

i2 = i1 * p + d
   = (i0 * p + d) * p + d
   = i0*p**2 + p * d + d

in = i0*p**n + d*p**(n-1) + d*p**(n-2) + ... + d*p + d

sum(p**k) for k=0 to n == (p**(n+1) - 1) / (p - 1)
in = i*p**n + d * (p**(n+1)-1) / (p-1)
"""
def affine_pow(p, d, k, m):
    """
    Calculates pk, dk for f^k(x) = pk * x + dk
    where: f(x) = (px + d) % m

    Results are modulo m
    """
    if k == 0:
        return 1, 0
    if k % 2 == 0:
        return affine_pow(p*p % m, (p*d + d) % m, k/2, m)
    else:
        p2, d2 = affine_pow(p, d, k-1, m)
        return p*p2 % m, (d2*p + d) % m


def mod_inv(a, m):
    t, t2 = 0, 1
    r, r2 = m, a
    while r2:
        q = r / r2
        t, t2 = t2, t - q*t2
        r, r2 = r2, r - q*r2
    if r > 1: raise ValueError("No inverse")
    if t < 0: t += m
    return t


commands = parse_file("22.txt")
p, d = process_transforms(commands)
s = 2019 * p + d
print s % 10007

L = 119315717514047
T = 101741582076661
p, d = affine_pow(p, d, T, L)
"""
2020 = X * p + d mod L
X = p**-1 * (2020 - d) mod L
"""
pinv = mod_inv(p, L)
print (2020 - d) * pinv % L
