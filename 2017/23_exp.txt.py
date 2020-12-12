"""
Approximate Python code for the input
"""

b = 108400
c = b + 17000
while b != c:
    f = 1
    d = 2
    while d != b:
        e = 2
        while e != b:
            if d*e == b:
                f = 0
            e += 1
        d += 1
    if f == 0:
        h += 1
    b += 17


"""
The inner most loop:

e = 2
while e != b:
    if d*e == b:
        f = 0
    e += 1

Sets f to 0 if b is a multiple of d
"""

b = 108400
c = b + 17000
while b != c:
    f = 1
    d = 2
    while d != b:
        if b % d == 0:
            f = 0
        d += 1
    if f == 0:
        h += 1
    b += 17


"""
f = 1
d = 2
while d != b:
    if b % d == 0:
        f = 0
    d += 1

This sets f to zero if there is a d < b s.t. b % d == 0
i.e. f is zero if b is not prime
i.e. f = is_prime(b)
"""

# So, this code can be written as:
sum(not is_prime(n) for n in range(108400, 108400 + 17000, 17))
