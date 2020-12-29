import re


REV = "r"
CUT = "c"
INC = "i"


def parse_line(line):
    if "new stack" in line:
        return (REV, None)
    elif "increment" in line:
        return (INC, int(re.findall("\d+", line)[-1]))
    elif "cut" in line:
        return (CUT, int(re.findall("-*\d+", line)[-1]))
    raise ValueError("Bad line '%s'" % line)


def parse_file(filename):
    with open(filename) as f:
        return [parse_line(l) for l in f]


def rev(cards):
    return list(reversed(cards))


def cut(cards, n):
    return cards[n:] + cards[:n]


def inc(cards, n):
    new_cards = [0] * len(cards)
    i = 0
    for c in cards:
        new_cards[i] = c
        i += n
        i %= len(cards)
    return new_cards


commands = parse_file("22.txt")
initial_cards = list(range(10007))
cards = initial_cards
for cmd, v in commands:
    if cmd == REV:
        cards = rev(cards)
    elif cmd == CUT:
        cards = cut(cards, v)
    elif cmd == INC:
        cards = inc(cards, v)
print cards.index(2019)
