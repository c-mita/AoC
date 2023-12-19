"""
Part 1 is simple; just run each part through the rules to determine which ones
are "valid" (finally evaluate to "A").

For Part 2, we make each "sub-rule" (pattern) within a "workflow" (rule)
operate on an interval.

In general, each pattern splits the current interval into two:
    A "matching" half.
    An "unmatching" half.

The matching half is sent to the target rule pointed to by the pattern and we
evaluate that recursively.
The unmatching half is sent to the next pattern in the current rule.
(Obviously either of these can be empty, in which case we skip it).

An interval that is accepted is yielded from our generator.
An interval that is rejected is simply dropped.

Finally we sum the areas of all 4D intervals returned.
It is safe to assume these intervals do not overlap because the rules are
strictly filtering operations that just partition up the input interval.
"""


def parse_file(filename):
    def parse_part(line):
        parts = line[1:-1].split(",")
        return {part.split("=")[0]:int(part.split("=")[1]) for part in parts}

    def parse_rule(line):
        key, patterns = line[:-1].split("{")
        patterns = patterns.split(",")
        return key, patterns

    rules = {}
    parts = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line[0] == "{":
                parts.append(parse_part(line))
            else:
                key, data = parse_rule(line)
                rules[key] = data
    return rules, parts


def evaluate_rule(patterns, part):
    for pattern in patterns:
        if ":" not in pattern:
            return pattern
        subject, op = pattern[0], pattern[1]
        value, target = pattern[2:].split(":")
        value = int(value)

        test_value = part[subject]
        if op == "<" and test_value < value:
            return target
        if op == ">" and test_value > value:
            return target

def test_part(part, rules, start_rule):
    rule = rules
    target = start_rule
    while target != "A" and target != "R":
        target = evaluate_rule(rules[target], part)
    return target == "A"


def passing_intervals(rules, start_rule):
    key_idx_map = {"x":0, "m":1, "a":2, "s":3}

    def evaluate_rule(interval, key):
        if key == "A":
            yield interval
            return
        elif key == "R":
            return
        for pattern in rules[key]:
            if ":" not in pattern:
                yield from evaluate_rule(interval, pattern)
                return
            subject, op = pattern[0], pattern[1]
            value, target = pattern[2:].split(":")
            value = int(value)
            idx = key_idx_map[subject]
            lx, hx = interval[idx][0], interval[idx][1]
            matching = None
            if op == ">" and hx > value:
                matching = (max(lx, value+1), hx)
                unmatching = (min(lx, value), value)
            if op == "<" and lx < value:
                matching = (lx, min(hx, value-1))
                unmatching = (value, max(hx, value))
            if matching:
                matching_full = list(interval)
                matching_full[idx] = matching
                matching = tuple(matching_full)
                yield from evaluate_rule(matching, target)
                if unmatching[0] == unmatching[1]:
                    return
                unmatching_full = list(interval)
                unmatching_full[idx] = unmatching
                unmatching = tuple(unmatching_full)
                interval = unmatching

    start_interval = ((1, 4000),) * 4
    return list(evaluate_rule(start_interval, start_rule))


def interval_size(interval):
    p = 1
    for l, h in interval:
        p *= (h - l) + 1
    return p


rules, parts = parse_file("19.txt")
start_key = "in"
passed = (part for part in parts if test_part(part, rules, start_key))
part_sum = sum(sum(v for v in part.values()) for part in passed)
print(part_sum)

intervals = passing_intervals(rules, start_key)
valid = sum(interval_size(interval) for interval in intervals)
print(valid)
