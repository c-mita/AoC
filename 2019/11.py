import collections
import intcode


def rotate_left(d):
    return (d[1], -d[0])

def rotate_right(d):
    return (-d[1], d[0])


def run_robot(vm):
    panels = collections.defaultdict(int)
    px, py = 0, 0
    dx, dy = 0, -1
    try:
        vm_out = vm.run_generator()
        while True:
            v, d = next(vm_out), next(vm_out)
            panels[(px, py)] = v
            dx, dy = rotate_right((dx, dy)) if d else rotate_left((dx, dy))
            px, py = px+dx, py+dy
            vm.input_stream = iter([panels[(px, py)]])
    except StopIteration:
        pass
    return panels


def panels_to_string(panels):
    idxs = panels.keys()
    xmax, ymax = max(x for x, y in idxs), max(y for x, y in idxs)
    rows = []
    for y in range(ymax+1):
        row = ""
        for x in range(xmax+1):
            row += "#" if panels[(x, y)] == 1 else " "
        rows.append(row)
    return "\n".join(r.strip() for r in rows)



code = intcode.parse_input("11.txt")

vm = intcode.IntcodeVm(code, iter([0]))
painted_panels = run_robot(vm)
print len(painted_panels)

vm = intcode.IntcodeVm(code, iter([1]))
painted_panels = run_robot(vm)
print panels_to_string(painted_panels)
