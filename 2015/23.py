"""
Well this was easy - just implement the VM.
No analysis required for part 2, just run with a different initial state.
"""


import collections


State = collections.namedtuple(
        "State",
        ["pc", "a", "b"],
)

NULL_STATE = State(pc=0, a=0, b=0)


def parse_offset(offset):
    polarity = 1 if offset[0] == "+" else -1
    value = int(offset[1:])
    return polarity * value


def get_register(state, register):
    if register == "a":
        return state.a
    elif register == "b":
        return state.b
    else:
        raise ValueError(f"Bad register '{register}'.")


def op_hlf(arg, state):
    a = state.a
    b = state.b
    if arg == "a":
        a //= 2
    elif arg == "b":
        b //= 2
    else:
        raise ValueError(f"Bad argument '{arg}'")
    return State(pc=state.pc+1, a=a, b=b)


def op_tpl(arg, state):
    a = state.a
    b = state.b
    if arg == "a":
        a *= 3
    elif arg == "b":
        b *= 3
    else:
        raise ValueError(f"Bad argument '{arg}'")
    return State(pc=state.pc+1, a=a, b=b)


def op_inc(arg, state):
    a = state.a
    b = state.b
    if arg == "a":
        a += 1
    elif arg == "b":
        b += 1
    else:
        raise ValueError(f"Bad argument '{arg}'")
    return State(pc=state.pc+1, a=a, b=b)


def op_jmp(arg, state):
    pc = state.pc
    pc += parse_offset(arg)
    return State(pc=pc, a=state.a, b=state.b)
    

def op_jie(arg, state):
    r, offset = arg.split(", ")
    pc = state.pc
    offset = parse_offset(offset)
    if get_register(state, r) % 2 == 0:
        pc += offset
    else:
        pc += 1
    return State(pc=pc, a=state.a, b=state.b)


def op_jio(arg, state):
    r, offset = arg.split(", ")
    pc = state.pc
    offset = parse_offset(offset)
    if get_register(state, r) == 1:
        pc += offset
    else:
        pc += 1
    return State(pc=pc, a=state.a, b=state.b)


def step_program(program, state):
    pc = state.pc
    if not (0 <= pc < len(program)):
        raise ValueError(f"Invalid address '{pc}'")
    instruction = program[pc]
    ins, arg = instruction.split(" ", maxsplit=1)
    if ins == "hlf":
        return op_hlf(arg, state)
    elif ins == "tpl":
        return op_tpl(arg, state)
    elif ins == "inc":
        return op_inc(arg, state)
    elif ins == "jmp":
        return op_jmp(arg, state)
    elif ins == "jie":
        return op_jie(arg, state)
    elif ins == "jio":
        return op_jio(arg, state)
    else:
        raise ValueError(f"Bad instruction {instruction}")


def run_program(program, state=NULL_STATE):
    while 0 <= state.pc < len(program):
        state = step_program(program, state)
    return state


test_program = [
    "inc a",
    "jio a, +2",
    "tpl a",
    "inc a",
]

program = test_program
with open("23.txt") as f:
    program = [l.strip() for l in f]

state = run_program(program)
print(state.b)

state = run_program(program, state=State(pc=0, a=1, b=0))
print(state.b)
