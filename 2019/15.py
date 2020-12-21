import intcode


REVERSE_COMMANDS = {1:2, 2:1, 3:4, 4:3}


code = intcode.parse_input("15.txt")
vm = intcode.IntcodeVm(code)


def map_space(vm, space=None, path=[], pos=(0, 0)):
    if space is None:
        space = {pos:(1, 0)}
    distance = len(path) + 1
    for delta, cmd in zip([(0,-1), (0,1), (-1,0), (1,0)], [1, 2, 3, 4]):
        np = (pos[0] + delta[0]), (pos[1] + delta[1])
        if np in space:
            continue
        result = vm.run_for_input(cmd)[0]
        if np not in space or space[np][1] > distance:
            space[np] = result, distance

        if result == 0:
            continue
        map_space(vm, space, path + [cmd], np)

    if path:
        vm.run_for_input(REVERSE_COMMANDS[path[-1]])
    return space


def expand_front(front):
    new_front = set()
    for (px, py) in front:
        for p in [(px-1, py), (px+1, py), (px, py-1), (px, py+1)]:
            new_front.add(p)
    return new_front


def space_fill(space, start):
    empty = {k for k,(v,d) in space.items() if v == 1}
    front = expand_front({start}) & empty
    n = 0
    while empty:
        empty -= front
        front = expand_front(front) & empty
        n += 1
    return n


space = map_space(vm)
oxygen_key = [k for k, (v, d) in space.items() if v == 2][0]
print space[oxygen_key][1]
print space_fill(space, oxygen_key)
