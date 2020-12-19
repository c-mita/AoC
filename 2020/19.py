def parse_rule(line):
    key, values = line.strip().split(": ")
    key = int(key)
    if values == "\"a\"" or values == "\"b\"":
        return key, values.strip("\"")
    rules = []
    for rule in values.split(" | "):
        rules.append(tuple(map(int, rule.split())))
    return key, rules


def parse_file(filename):
    with open(filename) as f:
        rule_data, string_data = f.read().split("\n\n")
        rules = dict(parse_rule(l) for l in rule_data.split("\n"))
        return rules, string_data.strip().split("\n")


def match_subrule(sequence, rules, rule):
    n = 0
    for t in rule:
        v = match_sequence(sequence[n:], rules, t)
        if not v:
            return 0
        n += v
    return n


def match_sequence(sequence, rules, target=0):
    """
    Match the sequence greedily against rules.
    Returns the length of the leading subsequence that was fully matched.
    """
    if len(sequence) == 0:
        return 0
    v = sequence[0]
    rule = rules[target]
    if rule == "a" or rule == "b":
        return 1 if rule == v else 0
    for r in rule:
        v = match_subrule(sequence, rules, r)
        if v:
            return v
    return 0


rules, strings = parse_file("19.txt")
matched = [s for s in strings if match_sequence(s, rules) == len(s)]
print sum(1 for s in matched)
