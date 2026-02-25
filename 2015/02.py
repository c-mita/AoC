def parse_input(filename):
    boxes = []
    with open(filename) as f:
        for line in f:
            x, y, z = map(int, line.strip().split("x"))
            boxes.append((x, y, z))

    return boxes


def calc_area(box):
    x, y, z = box
    sides = x*y, x*z, y*z
    return 2 * sum(sides) + min(sides)


def calc_ribbon(box):
    def perimeter(x, y):
        return 2 * x + 2 * y
    x, y, z = box
    perimeters = (perimeter(x, y), perimeter(x, z), perimeter(y, z))
    return min(perimeters) + x * y * z


data = parse_input("02.txt")
total_area = sum(calc_area(box) for box in data)
print(total_area)

total_ribbon = sum(calc_ribbon(box) for box in data)
print(total_ribbon)
