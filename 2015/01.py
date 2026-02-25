def parse_input(filename):
    with open(filename) as f:
        return f.readlines()[0].strip()


def floor_number(data):
    return sum(1 if c == "(" else -1 for c in data)


def enters_floor(data, target):
    current = 0
    for n, c in enumerate(data):
        if c == "(":
            current += 1
        else:
            current -= 1
        if current == target:
            return n + 1
    raise ValueError("Never reaches target")

data = parse_input("01.txt")
floor = floor_number(data)
print(floor)

basement = enters_floor(data, -1)
print(basement)
