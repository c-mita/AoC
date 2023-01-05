"""
This didn't go as well as I hoped.
It appears that the intended solution was to inspect the input and analyse
it by hand to a degree; identifying roughly what each part does and operating
on simplified formulae.

I didn't want to do that. I wanted something that would work with "generalised"
inputs.

First we break up the input program into segments; each segment starts with
the input request and ends just before the next input.

We then proceed on a depth-first walk of the solution space, but at each
step we can run the remainder of the program in a VM using interval objects
for the remaining inputs to check if our current path can actually lead
to a solution.

We can safely assume division by intervals containig zero never happens
because we have been promised a well-formed program (which our input
should be) will never do this.

Unfortantly, this solution does not perform as well as I would like.
I suspect this would be significantly faster in a non-interpreted language,
but for my input, Part 2 takes close to three minutes to run (the first two
digits are 3 and 4, so a third of the possible space is examined).
Optimising the code may yield some improvements, but I don't think such changes
would yield a solution that runs anywhere near the target of a few seconds.
"""


def parse_file(filename):
    programs = []
    current = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith("inp"):
                current = [tuple(line.split(" "))]
                programs.append(current)
                continue
            op, dest, src = line.split(" ")
            if dest not in "wxyz":
                dest = int(dest)
            if src not in "wxyz":
                src = int(src)
            current.append((op, dest, src))
    return programs


def prune_program(program):
    stripped = []
    for step in program:
        if step[0] == "mul" and step[2] == 1:
            continue
        if step[0] == "div" and step[2] == 1:
            continue
        if step[0] == "add" and step[2] == 0:
            continue
        stripped.append(step)
    return stripped


class Interval:
    def __init__(self, low, high):
        if not low <= high:
            raise ValueError("Invalid ordering %s, %s" % (str(low), str(high)))
        self.low = low
        self.high = high

    def __str__(self):
        return "[%d, %d]" % (self.low, self.high)

    def __repr__(self):
        return "Interval(%d, %d)" % (self.low, self.high)

    @staticmethod
    def _unpack_other(other):
        if type(other) == Interval:
            return other.low, other.high
        else:
            return other, other

    def __add__(self, other):
        c, d = self._unpack_other(other)
        return Interval(self.low + c, self.high + d)

    def __radd__(self, other):
        c, d = self._unpack_other(other)
        return Interval(self.low + c, self.high + d)

    def __mul__(self, other):
        a, b = self.low, self.high
        c, d = self._unpack_other(other)
        if a >= 0 and c >= 0:
            return Interval(a * c, b * d)
        elif a >= 0 and d <= 0:
            return Intervals(a * d, b * c)
        elif b <= 0 and d <= 0:
            return Intervals(b * d, b * c)
        elif b <= 0 and c >= 0:
            return Intervals(b * c, a * d)
        # theif-elif chain is actually quicker than this
        # (surprsingly; the min-max stuff on four values is slow)
        # unreachable code follows
        products = a * c, a * d, b * c, b * d
        return Interval(min(products), max(products))

    def __rmul__(self, other):
        return self * other

    def __floordiv__(self, other):
        a, b = self.low, self.high
        c, d = self._unpack_other(other)
        if c > 0:
            return Interval(int(a // d), int(b // c))
        elif d < 0:
            return Interval(int(a // c), (b // d))
        else:
            raise ValueError("Range has a division by zero in it")

    def __rfloordiv__(self, other):
        if type(other) == Interval:
            return other // self
        else:
            return Interval(other, other) // self

    def __mod__(self, other):
        a, b = self.low, self.high
        if type(other) == Interval:
            raise NotImplementedError("Cannot be bothered to support this")
        if a < 0:
            raise ValueError("Cannot mod a value below zero")
        m = other
        if m > 0:
            # our range is restricted if the entire interval fits within the
            # range of the modulus
            # Technically, our mod could result in two intervals
            # [0, high % m] and [low % m, m-1]
            # but this is too complicated for me to want to implement
            # (+1 because a == b still requires a single value)
            if b - a + 1 < m and a % m <= b % m:
                return Interval(a % m, b % m)
            else:
                return Interval(0, m - 1)
        else:
            raise ValueError("Cannot mod by '%s'" % repr(other))

    def eql(self, other):
        # don't get to implement __eq__ here, unfortunately
        c, d = self._unpack_other(other)
        if self.low == c == self.high == d:
            return Interval(1, 1)
        elif self.low <= d and c <= self.high:
            return Interval(0, 1)
        return Interval(0, 0)


def run_program(program, in_values, state):
    state = dict(state)
    for step in program:
        if step[0] == "inp":
            state[step[1]] = next(in_values)
            continue
        op, p1, p2 = step
        v1 = state[p1]
        v2 = state[p2] if p2 in ["w", "x", "y", "z"] else p2
        if op == "add":
            state[p1] = v1 + v2
        elif op == "mul":
            state[p1] = v1 * v2
        elif op == "div":
            v = v1 // v2
            state[p1] = v
        elif op == "mod":
            state[p1] = v1 % v2
        elif op == "eql":
            if type(v1) == Interval:
                v = v1.eql(v2)
            elif type(v2) == Interval:
                v = v2.eql(v1)
            else:
                v = int(v1 == v2)
            state[p1] = v
        else:
            raise ValueError("Unknown operation '%s'" % op)
    return state


class BadPath(Exception): pass


def find_solution(programs, symbols):
    min_symbol = min(symbols)
    max_symbol = max(symbols)
    initial_state = {"w":0, "x":0, "y":0, "z":0}

    def interval_generator():
        while True:
            yield Interval(min_symbol, max_symbol)

    interval_gen = interval_generator()
    def walk(programs, matched, state):
        # check if our current path is, or leads to, a valid answer
        test_state = state
        for program in programs:
            test_state = run_program(program, interval_gen, test_state)
        z = test_state["z"]
        if type(z) == int:
            if z == 0:
                return matched
            raise BadPath
        if not (z.low <= 0 <= z.high):
            raise BadPath

        # path could be valid - step down one level
        for s in symbols:
            next_state = run_program(programs[0], iter([s]), state)
            matched.append(s)
            try:
                return walk(programs[1:], matched, next_state)
            except BadPath:
                pass
            matched.pop()
        raise BadPath

    match = walk(programs, [], initial_state)
    s = 0
    for v in match:
        s *= 10
        s += v
    return s


programs = parse_file("24_input.txt")
programs = [prune_program(p) for p in programs]
symbols = list(range(9, 0, -1))
match = find_solution(programs, symbols)
print(match)

symbols = list(range(1, 10))
match = find_solution(programs, symbols)
print(match)
