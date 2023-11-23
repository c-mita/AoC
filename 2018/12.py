def parse_input(filename):
    rules = []
    with open(filename) as f:
        initial_state = [c for c in next(f)[15:].strip()]
        next(f)
        for line in f:
            rule = line.strip().split(" => ")
            if rule[1] == "#":
                rules.append(tuple(rule[0]))
    return initial_state, rules


def step_state(i_start, i_end, state):
    next_state = {}
    for i in range(i_start, i_end):
        l2 = state.get(i-2, ".")
        l1 = state.get(i-1, ".")
        c = state.get(i, ".")
        r1 = state.get(i+1, ".")
        r2 = state.get(i+2, ".")

        for rule in rules:
            if (l2, l1, c, r1, r2) == rule:
                next_state[i] = "#"
                break
        else:
            next_state[i] = "."
    return i_start - 2, i_end + 2, next_state

initial_state, rules = parse_input("12_input.txt")
state = {}
for (idx, s) in enumerate(initial_state):
    state[idx] = s
initial_state = state

i_start = -2
i_end = len(state) + 2
for n in range(20):
    i_start, i_end, state = step_state(i_start, i_end, state)


print("".join([state[k] for k in sorted(state)]))
print(sorted(k for k in state if state[k] == "#"))
print(sum(k for (k, v) in state.items() if v == "#"))


"""
We appear to reach a "steady state" after 100 iterations or so - every step adds the same number to the sum.
We "average" just to help generalise a little...
"""

state = initial_state
i_start, i_end = -2, len(initial_state) + 2
deltas = []
s0, s1 = 0, 0
n_lead = 300
for n in range(n_lead):
    s0 = s1
    i_start, i_end, state = step_state(i_start, i_end, state)
    s1 = sum(k for (k, v) in state.items() if v == "#")
    deltas.append(s1 - s0)

average = sum(deltas[-100:]) // 100
print(s1 + average * (50*10**9 - n_lead))
