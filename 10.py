import re

BOT_T = 0
OUTPUT_T = 1

# bots are dict {bot : [value1, value2]}
# moves are dict {bot : (t1, d1), (t2, s2)} #type, value - e.g.

def parse_line(line, bots, moves):
    if line.startswith("bot"):
        b, d1, d2 = map(int, re.findall("[0-9]+", line))
        t1, t2 = re.findall("bot|output", line)[1:]
        moves[b] = ((BOT_T if t1 == "bot" else OUTPUT_T, d1),
            (BOT_T if t2=="bot" else OUTPUT_T, d2))
    elif line.startswith("value"):
        v, b = map(int, re.findall("[0-9]+", line))
        bots.setdefault(b, []).append(v)
    else:
        raise ValueError("Unknown instruction")

def parse_instructions(filename):
    bots = {}
    moves = {}
    with open(filename) as f:
        for line in f:
            parse_line(line, bots, moves)
    return bots, moves

def process_moves(bots, moves):
    outputs = {}
    while len(bots) > 0:
        for b, vs in bots.items():
            if len(vs) == 2:
                del bots[b]
                v1, v2 = sorted(vs)
                if v1 == 17 and v2 == 61:
                    print b
                (t1, d1), (t2, d2) = moves[b]
                d = bots if t1==BOT_T else outputs
                d.setdefault(d1, []).append(v1)
                d = bots if t2==BOT_T else outputs
                d.setdefault(d2, []).append(v2)
            elif len(vs) > 2:
                raise ValueError("BAD THINGS")
    return outputs

bots, moves = parse_instructions("10.txt")
outputs = process_moves(bots, moves)

print outputs[0][0] * outputs[1][0] * outputs[2][0]
