

"""
an = ~bn
b1b2b3
b1b2b3 0 a3a2a1
b1b2b3 0 a3a2a1 0 b1b2b3 1 a3a2a1
b1b2b3 0 a3a2a1 0 b1b2b3 1 a3a2a1 0 b1b2b3 0 a3a2a1 1 b1b2b3 1 a3a2a1
"""

"""
Length of string is after n steps is:
Ln+1 = 2*Ln + 1
=>
Ln = (2**n) * (L0 + 1) - 1
(solve the non-homogenous linear recurrence)
"""

from math import log

"""
l0 = len(INPUT)
L = lambda n: 2**n * (l0 + 1) - 1
RL = lambda d: log(float(d + 1) / (l0 + 1), 2)
print L(10)
print RL(272)
print L(3), L(4), L(RL(272))
"""

# really inefficient but i can't maths my way out of this quickly enough
def check_sum_simple(key, target_length):
    stream = list(key)
    while len(stream) < target_length:
        inv_stream = [1 if s == 0 else 0 for s in stream[::-1]]
        stream = stream + [0] + inv_stream
    stream = stream[:target_length]
    checksum = []
    check_in = stream
    while len(checksum) % 2 == 0:
        checksum = []
        for a, b in zip(check_in[:-1:2], check_in[1::2]):
            checksum.append(a ^ b)
        check_in = checksum
    return ''.join(str(0 if d else 1) for d in checksum)

INPUT = "10000"
INPUT = "10001001100000001"

key = [int(k) for k in INPUT]
#print check_sum(key, 272)
print check_sum_simple(key, 272)
print check_sum_simple(key, 35651584)
