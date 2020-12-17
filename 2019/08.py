def parse_file(filename):
    with open(filename) as f:
        return map(int, "".join(l.strip() for l in f))

sx, sy = 25, 6
size = sx * sy

data = parse_file("08.txt")
layers = [data[size*n:size*(n+1)] for n in range(len(data)/size)]

min_layer = 0x7fffffff, None
for layer in layers:
    l = sum(1 for v in layer if not v)
    min_layer = min_layer if min_layer[0] < l else (l, layer)

min_n, layer = min_layer
print sum(1 for v in layer if v == 1) * sum(1 for v in layer if v == 2)


image = [2] * size
for layer in reversed(layers):
    for (n, v) in enumerate(layer):
        if v != 2:
            image[n] = v

for row in (image[sx*n:sx*(n+1)] for n in range(sy)):
    print "".join([" " if c == 0 else "#" for c in row]).strip()
