from collections import namedtuple

COPY = "cpy"
JNZ = "jnz"
INC = "inc"
DEC = "dec"
TGL = "tgl"
MUL = "mul"
ADD = "add"

IP = "ip"
A, B, C, D = "a", "b", "c", "d"

Instruction = namedtuple("Instruction", "op, args")

def process_line(line):
    elements = line.split()
    regs = {A, B, C, D}
    op = elements[0]
    if op == COPY or op == JNZ or op == MUL or op == ADD:
        e1, e2 = elements[1], elements[2]
        a1 = e1 if e1 in regs else int(e1)
        a2 = e2 if e2 in regs else int(e2)
        return Instruction(op, (a1, a2))
    elif op == INC or op == DEC or op == TGL:
        e = elements[1]
        a = e if e in regs else int(e)
        return Instruction(op, (a,))

def parse_file(filename):
    with open(filename) as f:
        return [process_line(line) for line in f]

def toggle(instruction):
    op, args = instruction.op, instruction.args
    if op == INC:
        return Instruction(DEC, args)
    elif op == DEC or op == TGL:
        return Instruction(INC, args)
    elif op == COPY:
        return Instruction(JNZ, args)
    elif op == JNZ:
        return Instruction(COPY, args)
    else:
        raise ValueError("Unknown opcode %s" % op)

def run(initial_state, code):
    state = dict(initial_state)
    code = list(code)
    while state[IP] < len(code):
        instruction = code[state[IP]]
        op, args = instruction.op, instruction.args
        if (op == INC or op == DEC) and \
                args[0] not in state:
            state[IP] += 1
            continue
        elif op == INC: state[args[0]] += 1
        elif op == DEC: state[args[0]] -= 1
        elif op == MUL or op == ADD:
            a1, a2 = args
            if a1 not in state:
                state[IP] +=1
                continue
            op2 = state[a2] if a2 in state else a2
            if op == MUL:
                state[a1] *= op2
            else:
                state[a1] += op2
        elif op == COPY:
            a1, a2 = args
            if a2 not in state:
                state[IP] += 1
                continue
            op1 = state[a1] if a1 in state else a1
            state[a2] = op1
        elif op == TGL:
            op1 = state[args[0]] if args[0] in state else args[0]
            p = state[IP] + op1
            if 0 <= p < len(code):
                code[p] = toggle(code[p])
        elif op == JNZ:
            a1, a2 = args
            op1 = state[a1] if a1 in state else a1
            op2 = state[a2] if a2 in state else a2
            if op1 != 0:
                state[IP] += op2
                continue
        else:
            raise ValueError("Unknown opcode %s" % op)
        state[IP] += 1
    return state

test_code = parse_file("23_test.txt")
initial_state = {A:7, B:0, C:0, D:0, IP:0}
print run(initial_state, test_code)

code = parse_file("23.txt")
initial_state = {A:7, B:0, C:0, D:0, IP:0}
print run(initial_state, code)
code = parse_file("23_altered.txt")
print run(initial_state, code)

code = parse_file("23_altered.txt")
initial_state = {A:12, B:0, C:0, D:0, IP:0}
print run(initial_state, code)
