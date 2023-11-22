import re

"""
Nothing clever.

For part 1 we just execute each allowed operation and check if the result
matches the one we're given.

For part 2, we create two maps:
    {code : set(potential_functions)}
    {func : set(potential_codes)}

We then look to see if there are instances where, for a given key in one of
the maps, one of the sets only has a single value. This allows us to eliminate
that (op_code, function) pair from everywhere in both maps.

We do this for as long as possible and assume this generates a complete map.
"""


def process_file(filename):
    with open(filename) as f:
        lines = "".join(f.readlines())
    transforms, program = lines.split("\n\n\n")
    transforms = transforms.split("\n\n")
    transforms = [t.split("\n") for t in transforms]

    def ints(string):
        return tuple(map(int, re.findall("[0-9]+", string)))
    transforms = [(ints(b), ints(i), ints(a)) for b,i,a in transforms]
    program = [ints(line) for line in program.split("\n") if line]

    return transforms, program


def perform_op(state, op, func):
    _op, a, b, c = op
    new_state = list(state)
    new_state[c] = func(state, op)
    return tuple(new_state)

def addr(state, op):
    return perform_op(state, op, lambda s, o: s[o[1]] + s[o[2]])

def addi(state, op):
    return perform_op(state, op, lambda s, o: s[o[1]] + o[2])

def mulr(state, op):
    return perform_op(state, op, lambda s, o: s[o[1]] * s[o[2]])

def muli(state, op):
    return perform_op(state, op, lambda s, o: s[o[1]] * o[2])

def andr(state, op):
    return perform_op(state, op, lambda s, o: s[o[1]] & s[o[2]])

def andi(state, op):
    return perform_op(state, op, lambda s, o: s[o[1]] & o[2])

def orr(state, op):
    return perform_op(state, op, lambda s, o: s[o[1]] | s[o[2]])

def ori(state, op):
    return perform_op(state, op, lambda s, o: s[o[1]] | o[2])

def setr(state, op):
    return perform_op(state, op, lambda s, o: s[o[1]])

def seti(state, op):
    return perform_op(state, op, lambda s, o: o[1])

def gtir(state, op):
    return perform_op(state, op, lambda s, o: 1 if o[1] > s[o[2]] else 0)

def gtri(state, op):
    return perform_op(state, op, lambda s, o: 1 if s[o[1]] > o[2] else 0)

def gtrr(state, op):
    return perform_op(state, op, lambda s, o: 1 if s[o[1]] > s[o[2]] else 0)

def eqir(state, op):
    return perform_op(state, op, lambda s, o: 1 if o[1] == s[o[2]] else 0)

def eqri(state, op):
    return perform_op(state, op, lambda s, o: 1 if s[o[1]] == o[2] else 0)

def eqrr(state, op):
    return perform_op(state, op, lambda s, o: 1 if s[o[1]] == s[o[2]] else 0)

OPERATIONS = [addr, addi, mulr, muli, andr, andi, orr, ori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

def matching_ops(before, op, after):
    matches = []
    for f in OPERATIONS:
        if after == f(before, op):
            matches.append(f)
    return matches

def run_program(op_map, program):
    state = (0, 0, 0, 0)
    def step(operation, state):
        func = op_map[operation[0]]
        return func(state, operation)
    for line in program:
        state = step(line, state)
    return state


def identify_ops(transforms):
    op_map = {}
    reverse_opmap = {f:set() for f in OPERATIONS}
    fixed_map = {}
    for op_code in range(16):
        op_map[op_code] = set(OPERATIONS)
    for before, op, after in transforms:
        op_code = op[0]
        matches = matching_ops(before, op, after)
        op_map[op_code] &= set(matches)
        for m in matches:
            reverse_opmap[m].add(op_code)
    while True:
        func_to_remove = None
        opcode_to_remove = None
        # we look for instances where only one value can match an op_code
        # If we can't find those, we look for where a function matches a
        # a single op code.
        for op_code, choices in op_map.items():
            if len(choices) == 1:
                func_to_remove = choices.pop()
                opcode_to_remove = op_code
                break
        else:
            for func, choices in reverse_opmap.items():
                if len(choices) == 1:
                    opcode_to_remove = choices.pop()
                    func_to_remove = func
                    break
            else:
                break

        if func_to_remove is None != opcode_to_remove is None:
            raise ValueError("WTF?")
        if func_to_remove is not None:
            if opcode_to_remove in fixed_map:
                raise ValueError("%d already fixed" % opcode_to_remove)
            fixed_map[opcode_to_remove] = func_to_remove
            del reverse_opmap[func_to_remove]
            del op_map[opcode_to_remove]
            for choices in op_map.values():
                choices.discard(func_to_remove)
            for choices in reverse_opmap.values():
                choices.discard(opcode_to_remove)

    if op_map or reverse_opmap:
        raise ValueError("Incomplete identification")
    return fixed_map


transforms, program = process_file("16_input.txt")
matches = (matching_ops(*t) for t in transforms)
print(sum(1 if len(m) > 2 else 0 for m in matches))

op_map = identify_ops(transforms)
final_state = run_program(op_map, program)
print(final_state[0])
