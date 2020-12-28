import intcode
import itertools

CODE = intcode.parse_input("19.txt")


def check_coord(coord):
    vm = intcode.IntcodeVm(CODE, iter(coord))
    return vm.run()[0]


def find_box_start(start, n):
    n -= 1
    x, y = start
    while check_coord((x, y)):
        y += 1
    while True:
        y += 1
        while not check_coord((x, y)):
            x += 1
        if check_coord((x+n, y-n)):
            return x, y-n



points = []
for x, y in itertools.product(range(50), range(50)):
    if check_coord((x, y)):
        points.append((x, y))
print len(points)

x, y = points[-1]
beam = set(points)

bx, by = find_box_start((x, y), 100)
print bx * 10000 + by
