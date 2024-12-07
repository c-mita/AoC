def parse_file(filename):
    equations = []
    with open(filename) as f:
        for line in f:
            target, inputs = line.strip().split(": ")
            target = int(target)
            inputs = list(map(int, inputs.split(" ")))
            equations.append((target, inputs))
    return equations


def solvable(target, inputs, idx=0, current=0, ops=[]):
    if idx == len(inputs):
        return current == target
    if idx == 0:
        return solvable(
                target, inputs, idx=1, current=inputs[0], ops=ops)
    if current > target:
        return False

    v = inputs[idx]
    for op in ops:
        n = op(current, v)
        if solvable(target, inputs, idx=idx+1, current=n, ops=ops):
            return True
    return False


equations = parse_file("07.txt")
add = lambda x,y: x+y
mul = lambda x,y: x*y
s = 0
for target, inputs in equations:
    if solvable(target, inputs, ops=[add, mul]):
        s += target
print(s)

def cat(x, y):
    w = y
    while w:
        x *= 10
        w //= 10
    return x + y

s = 0
for target, inputs in equations:
    if solvable(target, inputs, ops=[add, mul, cat]):
        s += target
print(s)

