import collections

class IntcodeTerminate(Exception): pass

POS_MODE = 0
IM_MODE = 1
REL_MODE = 2


def null_input():
    while True: yield 0


def parse_input(filename):
    code = []
    with open(filename) as f:
        for line in f:
            code.extend(map(int, line.split(",")))
    return code


class IntcodeVm:
    def __init__(self, code, input_stream=null_input()):
        self.mem = collections.defaultdict(int)
        for (n, c) in enumerate(code):
            self.mem[n] = c
        self.pc = 0
        self.rel_base = 0
        self.input_stream = input_stream
        self.ops = {
                1:self.operator_add,
                2:self.operator_mul,
                3:self.operator_in,
                4:self.operator_out,
                5:self.operator_jump_true,
                6:self.operator_jump_false,
                7:self.operator_less_than,
                8:self.operator_equals,
                9:self.operator_rel_shift,
                99:self.operator_terminate
                }
        self.output = []


    def decode(self, opcode):
        op = opcode % 100
        modes = ((opcode/100) % 10, (opcode/1000) % 10, (opcode/10000) % 10)
        return op, modes


    def step(self):
        opcode = self.mem[self.pc]
        op, modes = self.decode(opcode)
        f = self.ops[op]
        return f(modes)


    def run(self):
        try:
            while True:
                v = self.step()
                if v is not None:
                    self.output.append(v)
        except IntcodeTerminate:
            pass
        return list(self.output)


    def run_generator(self):
        try:
            while True:
                v = self.step()
                if v is not None:
                    yield v
        except IntcodeTerminate:
            pass
        return


    def run_for_input(self, input_value=None):
        if input_value is None:
            input_value = []
        try:
            stream = iter(input_value)
        except TypeError:
            stream = iter([input_value])
        self.input_stream = stream
        output = []
        try:
            while True:
                try:
                    v = self.step()
                    if v is not None:
                        self.output.append(v)
                        output.append(v)
                except StopIteration:
                    return output
        except IntcodeTerminate:
            pass
        return output


    def operator_terminate(self, modes):
        raise IntcodeTerminate()


    def operator_add(self, modes):
        m1, m2, m3 = modes[0], modes[1], modes[2]
        a1, a2, a3 = self.mem[self.pc+1], self.mem[self.pc+2], self.mem[self.pc+3]

        a1 = a1 + self.rel_base if m1 == REL_MODE else a1
        a2 = a2 + self.rel_base if m2 == REL_MODE else a2
        a3 = a3 + self.rel_base if m3 == REL_MODE else a3

        v1 = a1 if m1 == IM_MODE else self.mem[a1]
        v2 = a2 if m2 == IM_MODE else self.mem[a2]

        assert m3 != IM_MODE

        r = v1 + v2

        self.mem[a3] = r
        self.pc += 4


    def operator_mul(self, modes):
        m1, m2, m3 = modes[0], modes[1], modes[2]
        a1, a2, a3 = self.mem[self.pc+1], self.mem[self.pc+2], self.mem[self.pc+3]

        a1 = a1 + self.rel_base if m1 == REL_MODE else a1
        a2 = a2 + self.rel_base if m2 == REL_MODE else a2
        a3 = a3 + self.rel_base if m3 == REL_MODE else a3

        v1 = a1 if m1 == IM_MODE else self.mem[a1]
        v2 = a2 if m2 == IM_MODE else self.mem[a2]

        assert m3 != IM_MODE

        r = v1 * v2

        self.mem[a3] = r
        self.pc += 4


    def operator_in(self, modes):
        assert modes[0] != IM_MODE
        v = next(self.input_stream)
        a1 = self.mem[self.pc + 1]
        a1 = self.rel_base + a1 if modes[0] == REL_MODE else a1
        self.mem[a1] = v
        self.pc += 2


    def operator_out(self, modes):
        m = modes[0]
        a = self.mem[self.pc + 1]
        a = a + self.rel_base if m == REL_MODE else a
        v = a if m == IM_MODE else self.mem[a]
        self.pc += 2
        return v


    def operator_jump_true(self, modes):
        m1, m2 = modes[0], modes[1]
        a1, a2 = self.mem[self.pc + 1], self.mem[self.pc + 2]

        a1 = a1 + self.rel_base if m1 == REL_MODE else a1
        a2 = a2 + self.rel_base if m2 == REL_MODE else a2

        v1 = a1 if m1 == IM_MODE else self.mem[a1]
        v2 = a2 if m2 == IM_MODE else self.mem[a2]

        self.pc = v2 if v1 != 0 else self.pc + 3


    def operator_jump_false(self, modes):
        m1, m2 = modes[0], modes[1]
        a1, a2 = self.mem[self.pc + 1], self.mem[self.pc + 2]

        a1 = a1 + self.rel_base if m1 == REL_MODE else a1
        a2 = a2 + self.rel_base if m2 == REL_MODE else a2

        v1 = a1 if m1 == IM_MODE else self.mem[a1]
        v2 = a2 if m2 == IM_MODE else self.mem[a2]

        self.pc = v2 if v1 == 0 else self.pc + 3


    def operator_less_than(self, modes):
        m1, m2, m3 = modes[0], modes[1], modes[2]
        assert m3 != IM_MODE
        a1, a2, a3 = self.mem[self.pc+1], self.mem[self.pc+2], self.mem[self.pc+3]

        a1 = a1 + self.rel_base if m1 == REL_MODE else a1
        a2 = a2 + self.rel_base if m2 == REL_MODE else a2
        a3 = a3 + self.rel_base if m3 == REL_MODE else a3

        v1 = a1 if m1 == IM_MODE else self.mem[a1]
        v2 = a2 if m2 == IM_MODE else self.mem[a2]

        self.mem[a3] = 1 if v1 < v2 else 0
        self.pc += 4


    def operator_equals(self, modes):
        m1, m2, m3 = modes[0], modes[1], modes[2]
        assert m3 != IM_MODE
        a1, a2, a3 = self.mem[self.pc+1], self.mem[self.pc+2], self.mem[self.pc+3]

        a1 = a1 + self.rel_base if m1 == REL_MODE else a1
        a2 = a2 + self.rel_base if m2 == REL_MODE else a2
        a3 = a3 + self.rel_base if m3 == REL_MODE else a3

        v1 = a1 if m1 == IM_MODE else self.mem[a1]
        v2 = a2 if m2 == IM_MODE else self.mem[a2]

        self.mem[a3] = 1 if v1 == v2 else 0
        self.pc += 4


    def operator_rel_shift(self, modes):
        m = modes[0]

        a = self.mem[self.pc + 1]
        a = a + self.rel_base if m == REL_MODE else a
        v = a if m == IM_MODE else self.mem[a]

        self.rel_base += v
        self.pc += 2
