"""
Simple recursive solution for Part 1. The entire problem set only requires
about 7 million choices, so we don't need to be too efficient in the
recursion code (for simplicity we recurse on every character in the pattern).

Part 2 seems much harder, but we can actually just memoize their recursion
function. Breaking the input apart into tuples instead of mutating data makes
part 1 slightly less efficient, but means we can use the exact same code
for both parts.

Runs in < 5 seconds on an Intel Macbook
"""


def parse_file(filename):
    data = []
    with open(filename) as f:
        for line in f:
            pattern, groups = line.strip().split(" ")
            groups = list(map(int, groups.split(",")))
            data.append((pattern, groups))
    return data


def count_solutions(pattern, groups):

    def cached(func):
        cache = {}
        def wrap(*args):
            if args in cache:
                return cache[args]
            v = func(*args)
            cache[args] = v
            return v
        return wrap

    @cached
    def recurse(remaining, current_run, unmatched):
        if not remaining:
            if len(unmatched) == 1 and current_run == unmatched[0]:
                return 1
            elif current_run == 0 and not unmatched:
                return 1
            return 0

        c = remaining[-1]
        if c == ".":
            if not current_run:
                return recurse(remaining[:-1], current_run, unmatched)
            if not unmatched or unmatched[-1] != current_run:
                return 0
            return recurse(remaining[:-1], 0, unmatched[:-1])
        elif c == "#":
            return recurse(remaining[:-1], current_run + 1, unmatched)
        elif c == "?":
            s1 = recurse(remaining[:-1] + "#", current_run, unmatched)
            s2 = recurse(remaining[:-1] + ".", current_run, unmatched)
            return s1 + s2
        else:
            raise ValueError("Unknown %s" % c)

    return recurse(pattern, 0, tuple(groups))


test_data = [
    ("???.###", [1, 1, 3]),
    (".??..??...?##.", [1, 1, 3]),
    ("#?#?#?#?#?#?#?#?", [1, 3, 1, 6]),
    ("????.#...#...", [4, 1, 1]),
    ("????.######..#####.", [1, 6, 5]),
    ("?###????????", [3, 2, 1]),
]

data = parse_file("12.txt")
solutions = sum(count_solutions(pattern, groups) for (pattern, groups) in data)
print(solutions)

expanded_solutions = []
for pattern, group in data:
    expanded_pattern = "?".join([pattern] * 5)
    expanded_group = group * 5
    expanded_solutions.append(count_solutions(expanded_pattern, expanded_group))

print(sum(expanded_solutions))
