from collections import namedtuple

COPY = "cpy"
JNZ = "jnz"
INC = "inc"
DEC = "dec"
OUT = "out"

IP = "ip"
A, B, C, D = "a", "b", "c", "d"

Instruction = namedtuple("Instruction", "op, args")
State = namedtuple("State", "IP, A, B, C, D")

def snapshot(state):
    return (state[IP], state[A], state[B], state[C], state[D], state[D])

def process_line(line):
    elements = line.split()
    regs = {A, B, C, D}
    op = elements[0]
    if op == COPY or op == JNZ:
        e1, e2 = elements[1], elements[2]
        a1 = e1 if e1 in regs else int(e1)
        a2 = e2 if e2 in regs else int(e2)
        return Instruction(op, (a1, a2))
    elif op == INC or op == DEC or op == OUT:
        e = elements[1]
        a = e if e in regs else int(e)
        return Instruction(op, (a,))

def parse_file(filename):
    with open(filename) as f:
        return [process_line(line) for line in f]

def step(state, instruction):
    out = None
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
        op2 = state[a2] if a2 in state else a2
        if op1 != 0:
            state[IP] += op2
            return None
    elif instruction.op == OUT:
        a1 = instruction.args[0]
        op1 = state[a1] if a1 in state else a1
        out = op1
    state[IP] += 1
    return out

def test_code(initial_state, code):
    output = []
    idx = 0
    state = dict(initial_state)
    snap = snapshot(state)
    observed = {}
    while snap not in observed:
        observed[snap] = idx
        out = step(state, code[state[IP]])
        if out is not None:
            output.append(out)
            idx += 1
        snap = snapshot(state)
    loop_start = observed[snap]
    return output

code = parse_file("25.txt")

test_a = 0
while 1:
    state = {A:test_a, B:0, C:0, D:0, IP:0}
    output = test_code(state, code)
    print test_a, output
    if (output * 2) == [0, 1] * len(output):
        # print test_a, output
        break
    #print test_a, test_code(state, code)
    test_a += 1
