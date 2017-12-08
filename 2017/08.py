"""
Instructions: (register, operator, operand, condition)
Condition: (arg1, comparitor, arg2)
"""

INC = "inc"
DEC = "dec"

EQ = "=="
NE = "!="
LT = "<"
LTE = "<="
GT = ">"
GTE = ">="

def parse_input(filename):
    def parse_line(line):
        operation, condition = (s.strip() for s in line.split("if"))
        o_a1, op, o_a2 = operation.split(" ")
        try: o_a2 = int(o_a2)
        except: pass
        c_a1, cond, c_a2 = condition.split(" ")
        try: c_a1 = int(c_a1)
        except: pass
        try: c_a2 = int(c_a2)
        except: pass
        return (o_a1, op, o_a2, (c_a1, cond, c_a2))
    with open(filename) as f:
        return [parse_line(line) for line in f]

def process(instructions):
    registers = {}
    max_val = 0
    for target, op, arg, cond in instructions:
        c_a1, c, c_a2 = cond
        if not isinstance(c_a1, int): c_a1 = registers.setdefault(c_a1, 0)
        if not isinstance(c_a2, int): c_a2 = registers.setdefault(c_a2, 0)
        cond_met = False
        if c == EQ: cond_met = c_a1 == c_a2
        elif c == NE: cond_met = c_a1 != c_a2
        elif c == LT: cond_met = c_a1 < c_a2
        elif c == LTE: cond_met = c_a1 <= c_a2
        elif c == GT: cond_met = c_a1 > c_a2
        elif c == GTE: cond_met = c_a1 >= c_a2
        else: raise ValueError("Unknown comparison %s" % c)
        if cond_met:
            if not isinstance(arg, int): arg = registers.setdefault(arg, 0)
            v = registers.setdefault(target, 0)
            v += arg if op == INC else -arg
            if v > max_val: max_val = v
            registers[target] = v
    return registers, max_val

instructions = [("b", INC, 5, ("a", GT, 1)),
        ("a", INC, 1, ("b", LT, 5)),
        ("c", DEC, -10, ("a", GTE, 1)),
        ("c", INC, -20, ("c", EQ, 10))]

instructions = parse_input("08_input.txt")

output_registers, max_val = process(instructions)
print sorted(output_registers.iteritems(), key=lambda (k, v): v)[-1]
print max_val
