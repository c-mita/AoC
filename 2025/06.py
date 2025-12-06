"""
Really just a fiddly parsing problem.
Part 1 is straight forward, but part 2 requires paying attention
to how things are formatted. "12 " and " 12" have different meanings
when interpreted within a column.
"""


class Calculation:
    def __init__(self, values, operation):
        self.values = values
        self.operation = operation

    def result(self):
        if self.operation == "+":
            return sum(self.values)
        elif self.operation == "*":
            r = 1
            for v in self.values:
                r *= v
            return r
        else:
            raise ValueError("Unknown operation '%s'" % self.operation)

    def __repr__(self):
        return f"Calculation({self.values}, {self.operation})"


def parse_problems(problems):
    if type(problems) == str:
        problems = problems.strip().split("\n")
    tasks = []
    for line in problems:
        for i, v in enumerate(line.split()):
            if len(tasks) <= i:
                tasks.append([])
            tasks[i].append(v)
    return [Calculation(list(map(int, t[:-1])), t[-1]) for t in tasks]


def parse_rotated_problems(problems):
    if type(problems) == str:
        problems = problems.strip("\n").split("\n")
    column_widths = [1]
    operations = [problems[-1][0]]
    for c in problems[-1][1:]:
        if c != " ":
            column_widths.append(1)
            operations.append(c)
        else:
            column_widths[-1] += 1
    # every column except the last one was given
    # an extra digit due to the space between operators
    for i in range(len(column_widths) - 1):
        column_widths[i] -= 1

    calculations = [Calculation([], op) for op in operations]
    for line in problems[:-1]:
        current = 0
        for n, width in enumerate(column_widths):
            digits = line[current:current + width]
            current += width + 1
            calc = calculations[n]

            for i, digit in enumerate(digits):
                if len(calc.values) <= i:
                    calc.values.append(0)
                if digit not in "0123456789":
                    continue
                calc.values[i] *= 10
                calc.values[i] += int(digit)
    return calculations


TEST_INPUT = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""

with open("06.txt") as f:
    data = [line.strip("\n") for line in f.readlines()]
    data = [line for line in data if line]

test_calculations = parse_problems(TEST_INPUT)
calculations = parse_problems(data)
result = sum(c.result() for c in calculations)
print(result)

test_rotated_calculations = parse_rotated_problems(TEST_INPUT)
rotated_calculations = parse_rotated_problems(data)
rotated_result = sum(c.result() for c in rotated_calculations)
print(rotated_result)
