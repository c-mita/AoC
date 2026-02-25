"""
Divide the the packages into three groups of equal weight.
Each subgroup must have Wg = Wt / 3.
First group wants minimal number of packages.

We can generate the optimum solution by generating
elements of the powerset of the items in order, where in order
means:
    * Fewest elements first, to optimise for the length.
    * Smallest elements considered before larger ones
      (to optimise for the product of the first group)

    i.e. (1, 2) is considered before (2, 3)
    and (3, 4) is considered before (1, 2, 3)

So, for each element of the powerset in this order, check if
we can recursively solve for the remaining elements.
Our first solution is an optimal one.
"""

import itertools


def subgroups(weight, elements):
    size = 1
    while size < len(elements):
        for g in itertools.combinations(elements, size):
            if sum(g) == weight:
                yield g
        size += 1


def division(items, n=3):
    items = sorted(items)
    max_weight = sum(items)
    if max_weight % n != 0:
        raise ValueError(f"{n} does not divide {max_weight}")
    target_weight = max_weight // n

    def _rec(remaining, to_go):
        if to_go == 1:
            if sum(remaining) != target_weight:
                raise ValueError("Bug")
            return (remaining,)
        for g in subgroups(target_weight, remaining):
            left = [v for v in remaining if v not in g]
            result = _rec(left, to_go-1)
            if result:
                return g, *result

    return _rec(items, to_go=n)
            

def product(it):
    p = 1
    for i in it:
        p *= i
    return p


test_input = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
items = test_input
with open("24.txt") as f:
    items = list(map(int, (l.strip() for l in f)))

solution = division(items, n=3)
print(product(solution[0]))
solution = division(items, n=4)
print(product(solution[0]))
