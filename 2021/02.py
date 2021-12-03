def parse_input(filename):
    steps = []
    with open(filename) as f:
        for l in f:
            direction, step = l.split(" ")
            direction = direction[0]
            step = int(step)
            if direction == "f":
                step = (step, 0)
            elif direction == "d":
                step = (0, step)
            elif direction == "u":
                step = (0, -step)
            else:
                raise ValueError("%s could not be parsed" % l)
            steps.append(step)
    return steps


steps = parse_input("02_input.txt")
pos, depth = 0, 0
for step in steps:
    pos += step[0]
    depth += step[1]
print(pos * depth)

aim, pos, depth = 0, 0, 0
for step in steps:
    aim += step[1]
    depth += aim * step[0]
    pos += step[0]
print (pos * depth)
