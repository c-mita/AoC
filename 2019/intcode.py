class IntcodeTerminate(Exception): pass


def parse_input(filename):
    code = []
    with open(filename) as f:
        for line in f:
            code.extend(map(int, line.split(",")))
    return code


class IntcodeVm:
    def __init__(self, code):
        self.mem = code
        self.pc = 0
        self.ops = {
                1:self.operator_add,
                2:self.operator_mul,
                99:self.operator_terminate
                }


    def step(self):
        opcode = self.mem[self.pc]
        f = self.ops[opcode]
        f()

    def run(self):
        try:
            while True: self.step()
        except IntcodeTerminate:
            pass

    def operator_terminate(self):
        raise IntcodeTerminate()

    def operator_add(self):
        a1, a2, a3 = self.mem[self.pc+1], self.mem[self.pc+2], self.mem[self.pc+3]
        v1, v2 = self.mem[a1], self.mem[a2]
        r = v1 + v2
        self.mem[a3] = r
        self.pc += 4

    def operator_mul(self):
        a1, a2, a3 = self.mem[self.pc+1], self.mem[self.pc+2], self.mem[self.pc+3]
        v1, v2 = self.mem[a1], self.mem[a2]
        r = v1 * v2
        self.mem[a3] = r
        self.pc += 4
