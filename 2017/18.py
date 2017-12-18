SET, ADD, MUL, MOD, SND, RCV, JGZ = "set", "add", "mul", "mod", "snd", "rcv", "jgz"
LAST_SND = "last_snd"

def parse_input(filename):
    def parse_line(line):
        op, args = line.split(" ", 1)
        def try_for_int(c):
            try:
                return int(c)
            except:
                return c
        args = tuple(try_for_int(a) for a in args.split())
        return op, args
    with open(filename) as f:
        return [parse_line(l) for l in f]


def step_p1(code, pc, registers):
    snd, recv = None, None
    op, operands = code[pc]
    o1 = operands[0]
    v1 = o1 if isinstance(o1, int) else registers.setdefault(o1, 0)
    if len(operands) > 1:
        o2 = operands[1]
        v2 = o2 if isinstance(o2, int) else registers.setdefault(o2, 0)
    if op == SND: registers[LAST_SND] = v1
    elif op == SET: registers[o1] = v2
    elif op == ADD: registers[o1] += v2
    elif op == MUL: registers[o1] *= v2
    elif op == MOD: registers[o1] %= v2
    elif op == RCV: recv = registers[LAST_SND] if v1 != 0 else None
    elif op == JGZ: pc += (v2 - 1) if v1 > 0 else 0 # v2-1 because we will always increment pc
    pc += 1
    return pc, recv

def step_p2(code, pc, registers, recv_queue):
    snd, recv = None, None
    op, operands = code[pc]
    o1 = operands[0]
    v1 = o1 if isinstance(o1, int) else registers.setdefault(o1, 0)
    if len(operands) > 1:
        o2 = operands[1]
        v2 = o2 if isinstance(o2, int) else registers.setdefault(o2, 0)
    if op == SND: snd = v1
    elif op == SET: registers[o1] = v2
    elif op == ADD: registers[o1] += v2
    elif op == MUL: registers[o1] *= v2
    elif op == MOD: registers[o1] %= v2
    elif op == RCV:
            if len(recv_queue) == 0: return pc, snd, True
            registers[o1] = recv_queue.pop(0)
    elif op == JGZ: pc += (v2 - 1) if v1 > 0 else 0 # v2-1 because we will always increment pc
    pc += 1
    return pc, snd, False

pc = 0
recv, snd = None, None
code = parse_input("18_input.txt")
registers = {}
while recv is None:
    pc, recv = step_p1(code, pc, registers)
print recv


registers_p0, registers_p1 = {"p":0}, {"p":1}
pc_0, pc_1 = 0, 0
rq_0, rq_1 = [], []
deadlock = False
sent_0, sent_1 = 0, 0
while not deadlock:
    p0_wait, p1_wait = False, False
    p0_steps, p1_steps = 0, 0
    while not p0_wait:
        pc_0, snd, p0_wait = step_p2(code, pc_0, registers_p0, rq_0)
        if snd is not None:
            sent_0 += 1
            rq_1.append(snd)
        p0_steps += 1
    while not p1_wait:
        pc_1, snd, p1_wait = step_p2(code, pc_1, registers_p1, rq_1)
        if snd is not None:
            sent_1 += 1
            rq_0.append(snd)
        p1_steps += 1
    deadlock = p1_steps == p0_steps == 1
print sent_1
