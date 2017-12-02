from collections import namedtuple

COPY = "cpy"
JNZ = "jnz"
INC = "inc"
DEC = "dec"

IP = "ip"
A, B, C, D = "a", "b", "c", "d"

Instruction = namedtuple("Instruction", "op, args")

def step(state, instruction):
    if instruction.op == COPY:
        a1, a2 = instruction.args
        op1 = state[a1] if a1 in state else a1
        state[a2] = op1
    elif instruction.op == INC:
        state[instruction.args[0]] += 1
    elif instruction.op == DEC:
        state[instruction.args[0]] -= 1
    elif instruction.op == JNZ:
        a1, a2 = instruction.args
        op1 = state[a1] if a1 in state else a1
        if op1:
            state[IP] += a2
            return
    state[IP] += 1

def process_line(line):
    elements = line.split()
    regs = {A, B, C, D}
    op = elements[0]
    if op == COPY or op == JNZ:
        e1, e2 = elements[1], elements[2]
        a1 = e1 if e1 in regs else int(e1)
        a2 = e2 if e2 in regs else int(e2)
        return Instruction(op, (a1, a2))
    elif op == INC or op == DEC:
        return Instruction(op, (elements[1],))

def run_program(initial_state, code):
    state = dict(initial_state)
    while state[IP] < len(code):
        step(state, code[state[IP]])
    return state

def parse_file(filename):
    with open(filename) as f:
        return [process_line(l) for l in f]

state = {A:0, B:0, C:0, D:0, IP:0}
instructions = parse_file("12.txt")

result = run_program(state, instructions)
print result[A]

state = {A:0, B:0, C:1, D:0, IP:0}
result = run_program(state, instructions)
print result[A]
