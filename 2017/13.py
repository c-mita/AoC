def parse_input(filename):
    with open(filename) as f:
        return [(int(l.strip()), int(s.strip())) for (l, s) in (line.split(":") for line in f)]

def caught_at_layer(layer, size):
    return layer % (2 * (size - 1)) == 0

layers = [(0,3), (1, 2), (4, 4), (6, 4)]
layers = parse_input("13_input.txt")
severity = sum(l*s for (l,s) in layers if caught_at_layer(l, s))
print severity

delay = 0
caught = layers
while len(caught) > 0:
    layers = [(l+1, s) for (l, s) in layers]
    caught = [l for l in layers if caught_at_layer(*l)]
    delay += 1
print delay
