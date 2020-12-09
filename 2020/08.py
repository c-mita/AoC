NOP = "nop"
ACC = "acc"
JMP = "jmp"


def parse_file(filename):
    out = []
    with open(filename) as f:
        for l in f:
            cmd, val = l.strip().split(" ")
            v = int(val[1:])
            v *= -1 if val[0] == "-" else 1
            out.append((cmd, v))
    return out


def run_to_loop(instructions, acc_val):
    seen = set()
    pc = 0
    while pc not in seen:
        if pc == len(instructions):
            return pc, acc_val
        seen.add(pc)
        cmd, val = instructions[pc]
        pc += 1
        if cmd == NOP:
            pass
        elif cmd == ACC:
            acc_val += val
        elif cmd == JMP:
            pc -= 1
            pc += val
    return pc, acc_val


def try_fixing(instructions):
    # this is an unsatisfying approach, but seems to be effective
    for n, command in enumerate(instructions):
        cmd, v = command
        if cmd == NOP or cmd == JMP:
            new = list(instructions)
            new[n] = (NOP if cmd == JMP else JMP, v)

            pc, acc_val = run_to_loop(new, 0)
            if pc == len(instructions):
                return acc_val


instructions = parse_file("08.txt")
print run_to_loop(instructions, 0)
print try_fixing(instructions)
