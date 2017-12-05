"""
This is surprisingly slow (~5 second run time).
We just simulate the jumps, but I would expect it to be a lot faster than this.
I suspect Python's array access/writing is hurting us due to boxed integer types.
I would expect a language with primitive array types would be much faster than this.
"""

def parse_input(filename):
    with open(filename) as f:
        return [int(l.strip()) for l in f]

def process(jump_instructions):
    jump_instructions = list(jump_instructions)
    pc = 0
    steps = 0
    l = len(jump_instructions)
    while 0 <= pc < l:
        steps += 1
        jump_instructions[pc] += 1
        pc += jump_instructions[pc] - 1
    return steps, jump_instructions

def process2(jump_instructions):
    jump_instructions = list(jump_instructions)
    pc = 0
    steps = 0
    try: # try-except IndexError is faster than while 0<=pc<l
        while True:
            prev = pc
            v = jump_instructions[pc]
            pc += v
            jump_instructions[prev] += 1 if v < 3 else -1
            steps += 1
    except IndexError: pass
    return steps, jump_instructions

test_instructions = [0, 3, 0, 1, -3]
instructions = parse_input("05_input.txt")
print process(instructions)[0]
print process2(instructions)[0]
