"""
Not too complex.
First we need to map a (row, column) pair to the "code number".
That is, its position in the sequence. The quadratic equations can be
derived by inspection.

Given a sequence "n", we can then calculate the value in that cell.
Vn = K^n * V0 mod M

Where:
    V0 = 20151125
    K = 252533
    M = 33554393

We can quickly calculate "binary" powers of K modulo M by squaring.
K^1, K^2, K^4, K^8, ....
So write "n" in binary and multiple the associated powers of K together
and take the result modulo M.
"""


def calculate_cell(row, column):
    # every row begins with "(r**2 - r) / 2 + 1"
    # the columns are then r0 + n*r + Tn
    # where Tn is the nth triangle number
    n = column - 1
    r0 = (row * row  - row) // 2 + 1
    t_n = (n * n + n) // 2

    rc = r0 + n * row + t_n
    return rc


def generate_kn(k, m, max_i):
    # generate powers of k of powers of 2
    # k^1, k^2, k^4, k^8, ...k^(2^i)
    # The resulting map is {i : k^(2^i)} mod M
    results = {0: k % m}
    i = 1
    k = k
    while i <= max_i:
        k *= k
        k %= m
        results[i] = k
        i += 1
    return results


def bits(value):
    result = {}
    bit = 0
    while value:
        result[bit] = value % 2
        bit += 1
        value >>= 1
    return result


K = 252533
M = 33554393
V = 20151125
coords = 2947, 3029

code_idx = calculate_cell(*coords)
# the first cell is not multipled by anything, so treat it as index 0, even
# though the problem statement has it as index 1
code_idx -= 1
binary = bits(code_idx)
max_bit = max(k for k in binary if binary[k])

k_powers = generate_kn(K, M, max_bit)

v = V
for b in binary:
    if not binary[b]:
        continue
    v *= k_powers[b]
    v %= M
print(v)
