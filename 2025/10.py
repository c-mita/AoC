"""
Not a great solution for Part 2, but it works.

For Part 1 we just BFS over the space. Switches are basically XOR operations.
We could just consider the power set of the switches and test, which really
ends up being the same thing. (There's no need to ever press a switch more than
once because a xor a == 0 and xor commutes).

Part 2 is an integer linear programming problem. We treat it as a recursive
backtracking one.

We try to order switches so that we process ones that "uniquely" affect components
of the target first. After this, we prioritise ones that affect components with large
values.

We can then guess the amount of times each switch is pressed recursively.

We can bound our guesses above and below by checking the components of the "remaining"
target after taking into account of previous guesses.

Runtime: ~25 minutes.
"""


import re


def parse_data(data):
    if type(data) == str:
        data = data.split("\n")
    for line in data:
        line = line.strip()
        if not line:
            continue
        target_pattern = re.findall(r"\[.*\]", line)[0][1:-1]
        switch_strings = re.findall(r"\(.*?\)", line)
        switches = []
        for switch in switch_strings:
            switches.append(tuple(map(int, re.findall("[0-9]+", switch))))
        joltages = re.findall("{.*}", line)[0]
        joltages = tuple(map(int, re.findall("[0-9]+", joltages)))
        yield target_pattern, switches, joltages


def toggle_switches(target, switches):

    def bfs(start=0, target=0, options=()):
        front = [start]
        visited = set(front)
        d = 0
        while front:
            next_front = set()
            for pos in front:
                if pos == target:
                    return d
                for option in options:
                    npos = pos ^ option
                    if npos in visited:
                        continue
                    next_front.add(npos)
                    visited.add(npos)
            front = next_front
            d += 1
        raise ValueError("Could not complete")

    t = 0
    # the LSB refers to the first target light
    # reverse the light order so this lines up with our
    # bit operations
    for s in reversed(target):
        t <<= 1
        if s == "#":
            t |= 1
    toggles = []
    for switch in switches:
        toggle = 0
        for v in switch:
            toggle |= 1 << v
        toggles.append(toggle)
    return bfs(0, t, toggles)


def solve_switches(target, switches):

    # we want to reorder the switches into an order that helps processing
    # We want the current switch to be the one selects "unique"
    # components in the target out of the remaining unprocessed switches.
    # In the event of a tie, prioritise the switch that affects the
    # component with the largest value
    def next_switch(remaining_switches):
        frequencies = [0] * len(target)
        for switch in remaining_switches:
            for s in switch:
                frequencies[s] += 1
        fidx, fvalue = min(((i, s) for (i, s) in enumerate(frequencies) if s > 0), key=lambda k: k[1])
        return max((switch for switch in remaining_switches if fidx in switch), key=lambda s:max(target[i] for i in s))
        #return max((switch for switch in remaining_switches if fidx in switch), key=len)

    switches = set(switches)
    ordered_switches = []
    while switches:
        switch = next_switch(switches)
        switches.remove(switch)
        ordered_switches.append(switch)

    switches = ordered_switches
    best_solution = 0x7FFFFFFF

    # Record if, for a given target component and switch index,
    # there are follow-up switches that affect that target component
    # i.e. if the current switch is not the last one affecting that
    # component
    have_other_switches = {}
    for idx, switch in enumerate(switches):
        for s in switch:
            have_other_switches[(s, idx)] = False
            for j in range(idx + 1, len(switches)):
                other = switches[j]
                if s in other:
                    have_other_switches[(s, idx)] = True


    def solve(switch_idx, reduced_target, presses=[]):
        nonlocal best_solution
        n_presses = sum(presses)
        if n_presses >= best_solution:
            return
        if n_presses + max(reduced_target) >= best_solution:
            return
        if switch_idx == len(switches):
            if all(v == 0 for v in reduced_target):
                best_solution = n_presses
                yield list(presses)
            return

        # need to work out how many times we can press the current button
        switch = switches[switch_idx]
        max_presses = min(reduced_target[i] for i in switch)

        # how many times must we press this button?
        min_presses = 0
        for s in switch:
            if not have_other_switches[(s, switch_idx)]:
                min_presses = max(min_presses, reduced_target[s])

        for n in range(max_presses, min_presses-1, -1):
            presses.append(n)
            new_target = list(reduced_target)
            for s in switch:
                new_target[s] -= n
            yield from solve(switch_idx + 1, new_target, presses)
            presses.pop()

    solutions = solve(0, target, [])
    v = min(solutions, key=lambda s: sum(s))
    return v


TEST_DATA = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""

test_entries = list(parse_data(TEST_DATA))
with open("10.txt") as f:
    entries = list(parse_data(f))

s = 0
for target, switches, joltages in entries:
    s += (toggle_switches(target, switches))
print(s)

#entries = test_entries
s = 0
for target, switches, joltages in entries:
    solution = solve_switches(joltages, switches)
    print(solution)
    s += sum(solution)
print(s)

