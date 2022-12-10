import collections


def parse_file(filename):
    instructions = []
    with open(filename) as f:
        for line in f:
            terms = line.strip().split()
            if terms[0] == "noop":
                instructions.append((terms[0], 0))
            else:
                instructions.append((terms[0], int(terms[1])))
    return instructions


def run_machine(instructions):
    x = 1
    cycle = 0
    state = {cycle:x}
    for cmd, value in instructions:
        if cmd == "noop":
            cycle += 1
            state[cycle] = x
        else:
            state[cycle+1] = x
            x += value
            state[cycle+2] = x
            cycle += 2
    return state


instructions = parse_file("10_input.txt")

state = run_machine(instructions)
print(sum(k * state[k-1] for k in [20, 60, 100, 140, 180, 220]))

grid = []
for r in range(6):
    row = []
    for c in range(40):
        row.append("..")
    grid.append(row)


for crt_pos in range(240):
    p = state[crt_pos]
    sprite = [p-1, p, p+1]
    c = crt_pos % 40
    if c in sprite:
        grid[int(crt_pos // 40)][crt_pos % 40] = "##"

display = "\n".join("".join(c for c in r) for r in grid)
print(display)
