"""
The first "inspect your input" problem for the year.
And also the first "let's create a VM" problem for the year.

Part 1 is easy, just create the VM.

Part 2...

First we must work out roughly what this program does.
Here's my input:

    bst A  -  B = A % 8
    bxl 6  -  B = B ^ 6
    cdv B  -  C = A / 2**B
    bxc 4  -  B = B ^ C
    bxl 7  -  B = B ^ 7
    adv 3  -  A = A / 2**3
    out B  -  print(B % 8)
    jnz 0  -  if (A==0) goto 0

In a more interpretible form:
    A = X  # input
    do:
        B = A & 7  # bottom three bits
        B ^= 6  # flip some bits
        C = A >> B  # shift down by B (at most 7 because a three bit number)
        B = B ^ C
        B = B ^ 7
        A >>= 3
        print(B & 7) # print the bottom three bits of B
    while A == 0

Every iteration of the loop prints a single digit and shifts A by three bits.
So to print out 16 symbols, we would need A to be at least 2**(3*15).
Which is quite a big number...

Notice that, for every iteration, only at most the lowest 10 bits of A are
involved in the output value (C = A >> B can be a shift of 7 at most, so only
the last 10 bits of A can affect the later value of B (since we only output the
last 3 bits of B)).

And then, every iteration just shifts A down by three.

So we can work backwards, the uppermost bits of A determine the last value output.
We "guess" the 10 bit combination for the last value. We test it by running the
program.

When we have one, we recurse with that "a" value.
For a given recursion level, we shift "a" left by three (a << 3) and start guessing
the next digit. We must always test for all symbols after the given one though.

Time is not as quick as I would like: ~7 seconds.
"""


import re

INPUT = """
Register A: 37293246
Register B: 0
Register C: 0

Program: 2,4,1,6,7,5,4,4,1,7,0,3,5,5,3,0
"""


def parse_data(data_str):
    values = list(map(int, re.findall("\d+", data_str)))
    return (values[0], values[1], values[2]), values[3:]

def combo_op(op, state):
    if 0 <= op <= 3:
        return op
    elif op == 4:
        return state[1]
    elif op == 5:
        return state[2]
    elif op == 6:
        return state[3]
    else:
        raise ValueError("Bad combo operand '%s'" % op)

def adv(op, state):
    i, a, b, c = state
    num = a
    den = 2 ** combo_op(op, state)
    na = a // den
    return (i+2, na, b, c)


def bxl(op, state):
    i, a, b, c = state
    b ^= op
    return (i+2, a, b, c)


def bst(op, state):
    i, a, b, c = state
    v = combo_op(op, state)
    b = v % 8
    return (i+2, a, b, c)


def bxc(op, state):
    i, a, b, c = state
    b = b ^ c
    return (i+2, a, b, c)


def jnz(op, state):
    i, a, b, c = state
    if a == 0:
        return (i+2, a, b, c)
    return (op, a, b, c)


def bdv(op, state):
    i, a, b, c = state
    ni, na, nb, nc = adv(op, state)
    return (ni, a, na, c)


def cdv(op, state):
    i, a, b, c = state
    ni, na, nb, nc = adv(op, state)
    return (ni, a, b, na)


def run_program(registers, program):
    state = (0,) + registers
    dispatch = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 6: bdv, 7: cdv}

    def run(state):
        while 0 <= state[0] < len(program) - 1:
            i = state[0]
            code = program[i]
            op = program[i + 1]
            if code == 5:
                v = combo_op(op, state)
                yield v % 8
                state = (i + 2, state[1], state[2], state[3])
            elif code in dispatch:
                state =  dispatch[code](op, state)
            else:
                raise ValueError("Bad opcode '%s'" % code)

    yield from run(state)


class NotFoundError(Exception): pass


def search_for_magic_value(program, initial_state):
    a, b, c = initial_state

    def dfs(idx, current_a):
        if idx < 0:
            return current_a
        current_a <<= 3
        for i in range(1024):
            a = current_a | i
            registers = (a, b, c)
            if list(run_program(registers, program)) == program[idx:]:
                next_a = a
                try:
                    return dfs(idx - 1, a)
                except NotFoundError:
                    continue
        else:
            raise NotFoundError

    return dfs(len(program)-1, 0)


state, program = parse_data(INPUT)

output = run_program(state, program)
print(",".join(map(str, output)))

calculated_a = search_for_magic_value(program, state)
print(calculated_a)
