"""
Not a good solution for Part 2; it's a WIP. But it does techincally work.

For Part 1 we just BFS over the space. Switches are basically XOR operations.
We could just consider the power set of the switches and test, which really
ends up being the same thing. (There's no need to ever press a switch more than
once because a xor a == 0 and xor commutes).

Part 2 is an integer linear programming problem. We treat it as a recursive
backtracking one.

The target is a vector T.
Elements of the vector are:
    T[i] == a0 * v0[i] + a1 * v1[i] + ... + an * vn[i]
Where some vj[i] == 0 (ignore those).
We need to find all values of the sequence (aj) that satisfy the constraint.
We then need the one that minimises sum(aj).

We start by guessing a values for the index i s.t. T[i] contains the fewest
number of "aj" coefficients in it. We choose a value and recurse.

This may not be the best way to do it.

Runtime: > 6 hours.
Yes, hours.
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


def add_switches(target, switches):
    # Write t[0] as sum(alpha_i * s_i[0])
    # Then we have a set of simultaneous equations
    # Use a recursive backtracker to solve
    # t_slots[0] is the [alpha_i, ...] that make up the coefficients for element

    initial_t = [set() for n in range(len(target))]
    coefficient_map = {}
    for i, switch in enumerate(switches):
        for s in switch:
            initial_t[s].add(i)
            if i not in coefficient_map:
                coefficient_map[i] = []
            coefficient_map[i].append(s)

    best_solution = 0x7FFFFFFF

    def solve(coefficients, t_slots, reduced_target, coefficient_sum=0):
        nonlocal best_solution
        if coefficient_sum > best_solution:
            return
        if not any(reduced_target):
            if coefficient_sum < best_solution:
                best_solution = coefficient_sum
            yield list(coefficients)
            return
        for v in reduced_target:
            # bad guess
            if v < 0:
                return
        slot_idx = None
        slot_min = 0x7FFFFFFF
        for idx in range(len(t_slots)):
            l = len(t_slots[idx])
            if l == 0:
                continue
            if l < slot_min:
                slot_idx = idx
                slot_min = l
        if slot_idx is None:
            # this leaf node failed
            return

        # we take a single value from this slot and guess its value
        slot = t_slots[slot_idx]
        # this is the coefficient we're guessing
        to_guess = slot.pop()
        for t_idx in coefficient_map[to_guess]:
            if t_idx != slot_idx:
                t_slots[t_idx].remove(to_guess)
        # if it's the last value in the element in the target vector, there's
        # only one guess to make
        if not len(slot):
            guess_range = (reduced_target[slot_idx],)
        else:
            max_guess = min(reduced_target[t_idx] for t_idx in coefficient_map[to_guess])
            guess_range = range(max_guess,-1,-1)
            #guess_range = range(max_guess+1)
        for guess in guess_range:

            for t_idx in coefficient_map[to_guess]:
                reduced_target[t_idx] -= guess

            coefficients[to_guess] = guess
            yield from solve(coefficients, t_slots, reduced_target, coefficient_sum=coefficient_sum+guess)
            coefficients[to_guess] = 0

            for t_idx in coefficient_map[to_guess]:
                reduced_target[t_idx] += guess

        for t_idx in coefficient_map[to_guess]:
            t_slots[t_idx].add(to_guess)

    coefficients = [0] * len(switches)
    solutions = solve(coefficients, initial_t, list(target))
    return min(solutions, key=lambda s: sum(s))


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
    solution = add_switches(joltages, switches)
    print(solution)
    s += sum(solution)
print(s)

