def parse_file(filename):
    code = []
    with open(filename) as f:
        for l in f:
            cmd, v1, v2 = l.strip().split()
            v2 = v2 if v2 in "abcdefgh" else int(v2)
            code.append((cmd, v1, v2))
    return code


def step_code(code, pc, registers):
    registers = dict(registers)
    cmd, op1, op2 = code[pc]
    pc += 1
    if str(op2) in "abcdefgh":
        op2 = registers[op2]
    if cmd == "set":
        registers[op1] = op2
    elif cmd == "sub":
        registers[op1] -= op2
    elif cmd == "mul":
        registers[op1] *= op2
    elif cmd == "jnz":
        if str(op1) in "abcdefgh":
            v = registers[op1]
        else:
            v = int(op1)
        if v != 0:
            pc += op2 - 1
    else:
        raise ValueError("Oops")
    return pc, registers


code = parse_file("23_input.txt")
registers = {k:0 for k in "abcdefgh"}
pc = 0

mul_count = 0
while 0 <= pc < len(code):
    if code[pc][0] == "mul": mul_count += 1
    pc, registers = step_code(code, pc, registers)
print mul_count


def is_prime(n):
    if n in [2, 3, 5, 7, 11]:
        return True
    for q in range(2, int(n**0.5) + 1):
        if n % q == 0:
            return False
    return True

# For the reasoning behind this, see 23_exp.txt.py
b = 84 * 100 + 100000
c = b + 17000
print sum(not is_prime(n) for n in range(b, c+1, 17))
