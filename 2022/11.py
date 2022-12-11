import re
import collections

"""
For part 1 just simulate the game as per the description.

For part 2, note that the monkeys check for division using primes
(proof is looking at the input), so let M by the product of all
the divisors used in the input.

Then we can simply perform another simulation but modulo M.
"""


def parse_file(filename):
    monkeys = {}
    items_map = {}
    with open(filename) as f:
        try:
            while True:
                n = int(re.findall("[0-9]+", next(f))[-1])
                items = list(map(int, re.findall("[0-9]+", next(f))))
                operation = parse_operation(next(f).split("= ")[1])
                test = parse_test([next(f), next(f), next(f)])
                monkeys[n] = (operation, test)
                items_map[n] = items
                next(f)
        except StopIteration:
            pass
    return monkeys, items_map


def parse_operation(text):
    parts = text.strip().split()
    left = parts[0] if parts[0] == "old" else int(parts[0])
    right = parts[2] if parts[2] == "old" else int(parts[2])
    return Operation(left, parts[1], right)


def parse_test(lines):
    test_line, true_line, false_line = lines
    test_v = int(re.findall("[0-9]+", test_line)[-1])
    true_v = int(re.findall("[0-9]+", true_line)[-1])
    false_v = int(re.findall("[0-9]+", false_line)[-1])
    return Test(test_v, true_v, false_v)


class Test:
    def __init__(self, divisor, true_target, false_target):
        self.divisor = divisor
        self.true_target = true_target
        self.false_target = false_target

    def evaluate(self, value):
        return self.true_target if value % self.divisor == 0 else self.false_target


class Operation:
    def __init__(self, left, operation, right):
        self.left = left
        self.right = right
        self.operation = operation

    def evaluate(self, old):
        l = old if self.left == "old" else self.left
        r = old if self.right == "old" else self.right
        if self.operation == "+":
            return l + r
        elif self.operation == "-":
            return l - r
        elif self.operation == "*":
            return l * r
        else:
            raise ValueError("Unknown operation %s" % self.operation)


def play_monkey_game(monkeys, items, rounds):
    items = {k:collections.deque(v) for (k,v) in items.items()}
    business = {k:0 for k in monkeys}
    for _ in range(rounds):
        for n in range(len(monkeys)):
            op, test = monkeys[n]
            for lvl in items[n]:
                worry = op.evaluate(lvl)
                worry = int(worry // 3)
                target = test.evaluate(worry)
                items[target].append(worry)
                business[n] += 1
            items[n].clear()
    return business


def play_worrisome_game(monkeys, items, rounds):
    m = 1
    for op, test in monkeys.values():
        m *= test.divisor

    items = {k:collections.deque(v) for (k, v) in items.items()}
    business = {k:0 for k in monkeys}
    for _ in range(rounds):
        for n in range(len(monkeys)):
            op, test = monkeys[n]
            for lvl in items[n]:
                worry = op.evaluate(lvl)
                worry %= m
                target = test.evaluate(worry)
                items[target].append(worry)
                business[n] += 1
            items[n].clear()
    return business


monkeys, items = parse_file("11_input.txt")

# Part 1
business = play_monkey_game(monkeys, items, 20)
business_values = sorted(business.values())
print(business_values[-1] * business_values[-2])

# Part 2
business = play_worrisome_game(monkeys, items, 10000)
business_values = sorted(business.values())
print(business_values[-1] * business_values[-2])
