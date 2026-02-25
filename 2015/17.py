"""
Straightforward.
Recursively solve counting the number of ways to reach a target using the
available set of containers.

At each step, we remove a container and see if we can solve the problem
using it and not using it. Base case is "target == 0" which permits a single
solution (using no containers). Running out is a failure (0 solutions).

Part 2 is identical, but we need to yield solutions and identify the shortest,
then count how many ways solve it using the same number of containers.

Two containers may have the same capacity but are still distinct for the
purposes of counting.
"""


def parse_input(filename):
    with open(filename) as f:
        return list(map(int, (l.strip() for l in f)))


def count_fill_options(containers, target):
    if target == 0:
        return 1
    if not containers:
        return 0
    container = containers.pop()
    number = count_fill_options(containers, target)
    number += count_fill_options(containers, target-container)
    containers.append(container)
    return number


def fill_options(containers, target):
    if target == 0:
        yield ()
        return
    if not containers:
        return
    container = containers.pop()
    for option in fill_options(containers, target):
        yield option
    for option in fill_options(containers, target-container):
        yield (container,) + option
    containers.append(container)


containers = parse_input("17.txt")

ways = count_fill_options(containers, 150)
print(ways)

options = sorted(fill_options(containers, 150), key=len)
quickest = [o for o in options if len(o) == len(options[0])]
print(len(quickest))
