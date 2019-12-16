test_input = [1, 2, 3, 4, 5, 6, 7, 8]

long_test_string = "69317163492948606335995924319873"
long_test_string = "02935109699940807407585447034323"

def parse_file(filename):
    with open(filename) as f:
        return parse_input_string(f.readlines()[0].strip())


def parse_input_string(s):
    return map(int, s)


def pattern_gen(pattern, repeats):
    while True:
        for p in pattern:
            for n in xrange(1, repeats+1):
                yield p


def fft_phase(signal):
    output = [0] * len(signal)
    for n in xrange(len(signal)):
        pg = pattern_gen([0, 1, 0, -1], n+1)
        next(pg)
        output[n] = abs(sum(s * p for (s, p) in zip(signal, pg))) % 10
    return output


signal = parse_input_string(long_test_string)
signal = parse_file("16_input.txt")

# Part 1 (kinda slow)
output = signal
for n in range(100):
    output = fft_phase(output)

print "".join(map(str, output[:8]))


# Part 2
"""
We cheat, kind of...
Represent the signal transformation as a Matrix T (len(s) * len(s))
Then the bottom right quadrant looks like (for a 16x16 matrix):
[[1, 1, 1, 1],
 [0, 1, 1, 1],
 [0, 0, 1, 1],
 [0, 0, 0, 1]]

The bottom left quadrant is the null matrix (all zeros)

So we are actually only interested in this reduced matrix, so long as our "offset"
puts us into the second half of the output result.

Take this matrix U, and we want U^100.
Note that U^n has values coming from the "nth" diagonal of Pascal's triangle
So we just need to calculate the first few million values from the 100th diagonal

Diagonal formula:
(n+k,k) = (n+k-1, k-1) * (n+k / k)
"""

def diagonal_gen(n):
    k = 0
    v = 1
    while True:
        yield v
        k += 1
        v *= (n + k)
        v /= k

offset = int("".join(map(str, signal[:7])))
signal *= 10000

mid_point = len(signal) / 2
assert offset > mid_point

subsignal = signal[mid_point:]
suboffset = offset - mid_point

values = []
for n in range(8):
    dg = diagonal_gen(99) # the 100th row (first row is 0)
    doffset = suboffset + n # tells us the row in the matrix U we are using
    out = sum((v * next(dg)) for v in subsignal[doffset:])
    out %= 10
    values.append(out)

print "".join(map(str, values))

# one liner because I can
#values = [sum((v * p) for (v, p) in zip(subsignal[suboffset + n:], diagonal_gen(99))) % 10 for n in range(8)]
#print "".join(map(str, values))
