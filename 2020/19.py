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


def match_rule(sequence, rules, rule):
    if not rule:
        yield sequence
    else:
        for seq in match(sequence, rules, rule[0]):
            for rem in match_rule(seq, rules, rule[1:]):
                yield rem


def match(sequence, rules, target=0):
    """
    Attempts to match a sequence to the given rules.
    Yielding "" indicates a full match.
    """
    if not sequence:
        return
    v = sequence[0]
    options = rules[target]
    if options == "a" or options == "b":
        if v == options:
            yield sequence[1:]
    else:
        for rule in options:
            for remainder in match_rule(sequence, rules, rule):
                yield remainder


test = {0:[(4,1,5)], 1:[(2,3),(3,2)], 2:[(4,4),(5,5)], 3:[(4,5),(5,4)], 4:"a", 5:"b"}

rules, strings = parse_file("19.txt")
matched = [s for s in strings if any(r == "" for r in match(s, rules))]
print len(matched)

rules[8] = [(42,), (42, 8)]
rules[11] = [(42, 31), (42, 11, 31)]
matched = [s for s in strings if any(r == "" for r in match(s, rules))]
print len(matched)
