"""
Part 1
Elf 1 gives 10 to every house
Elf 2 gives 20 to every second house
Elf 3 gives 30 to every third house
...
Elf n gives 10 * n to every nth house


House X receives:
sum(10 * k for k in divisors of X)
So we want the first X s.t. the 10 * sum(divisors(X)) >= input

Part 2
Elf 1 goes to [1, 50][::1]
Elf 2 goes to [2, 100][::2]
Elf 3 goes to [3, 150][::3]
...
Elf n goes to [n, n*50][::n]

Each elf gives 11 presents

X may be visited by any elf =< X and elf >= X/50
X may be visited by any X/50 <= elf <= X

X will be visited by any elf in [X/50, X] s.t.
elf is a divisor of X

So just go through every divisor of X and check if its
in that range - if so add it to the sum for X.
Repeat until such a sum exceeds the input / 11.

Not as fast as I would like - pypy makes quite a difference.
Maybe doing the dumb thing with proper arrays would be quicker.
"""


INPUT = 36000000

class PrimeSieve:
    def __init__(self, data):
        self.data = data

    def prime_factors(self, value):
        def _factors(value):
            v = value
            while v > 1:
                nv = self.data[v]
                yield v // nv
                v = nv
        return list(_factors(value))

    def divisors(self, value):
        factors = self.prime_factors(value)
        def _powerset(idx):
            if idx >= len(factors):
                yield ()
                return
            this = (factors[idx],)
            for partial in _powerset(idx+1):
                yield partial
                yield partial + this

        def _divisors():
            for option in _powerset(0):
                p = 1
                for v in option:
                    p *= v
                yield p
        return set(_divisors())


def sieved_primes(limit):
    data = [0] * (limit + 1)
    data[1] = 1
    n = 2
    while n < limit:
        if data[n] == 0:
            for i in range(1, limit // n):
                data[i * n] = i
        n += 1
    return PrimeSieve(data)


def divisor_sum(prime_factors):
    factors = {}
    for p in prime_factors:
        factors.setdefault(p, 0)
        factors[p] += 1

    product = 1
    for p, m in factors.items():
        v = p ** (m+1) - 1
        v //= p - 1
        product *= v
    return product


target = INPUT // 10
primes = sieved_primes(target)

best = 0
n = 0
while best < target:
    n += 1
    v = divisor_sum(primes.prime_factors(n))
    if v > best:
        best = v
print(n)


n = 0
target = INPUT // 11
best = 0
while best < target:
    n += 1
    l = n // 50
    divisors = primes.divisors(n)
    v = sum(e for e in divisors if l <= e <= n+1)
    if v > best:
        best = v
print(n)

