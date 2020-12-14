import re


def parse_instruction_block(ins_block):
    write, move, cont = ins_block
    write = int(write.split("value ")[1][:-1])
    move = -1 if "left" in move else 1
    cont = cont[-2]
    return write, move, cont


def parse_state_block(block):
    lines = block.split("\n")
    lines = [l.strip() for l in lines]
    state = lines[0][-2]
    if_0 = parse_instruction_block(lines[2:5])
    if_1 = parse_instruction_block(lines[6:9])
    return state, (if_0, if_1)


def parse_header(hdr):
    lines = hdr.split("\n")
    state = lines[0][-2]
    steps = int(re.findall("\d+", lines[1])[0])
    return state, steps


def parse_file(filename):
    instructions = {}
    with open(filename) as f:
        blocks = f.read().split("\n\n")
        start, state_blocks = blocks[0], blocks[1:]
        start_state, steps = parse_header(start)
        for state_block in state_blocks:
            s, i = parse_state_block(state_block)
            instructions[s] = i
        return start_state, instructions, steps


def step_machine(state, pc, tape, instructions):
    if_0, if_1 = instructions[state]
    ins = if_1 if tape.get(pc, 0) else if_0
    v, step, state = ins
    tape[pc] = v
    return pc + step, state


initial_state, instructions, steps = parse_file("25.txt")
initial_tape = {}
initial_pc = 0

tape = dict(initial_tape)
state = initial_state
pc = initial_pc
for n in range(steps):
    pc, state = step_machine(state, pc, tape, instructions)
print sum(1 for v in tape.values() if v)
