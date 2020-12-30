import collections
import itertools

import intcode


def queue_extractor(n, queues, flags):
    queue = queues[n]
    while True:
        if queue:
            flags[n] = True
            x, y = queue.popleft()
            yield x
            yield y
        else:
            flags[n] = False
            yield -1


def create_system(code):
    queues = collections.defaultdict(collections.deque)
    outputs = collections.defaultdict(list)
    flags = [True for n in range(50)]
    vms = [intcode.IntcodeVm(
        code,
        itertools.chain(
            iter([n]), queue_extractor(n, queues, flags)))
        for n in range(50)]
    return vms, queues, outputs, flags



def cycle_vms(vms, queues, outputs, flags):
    for n, vm in enumerate(vms):
        v = vm.step()
        if v is not None:
            outputs[n].append(v)
        if len(outputs[n]) == 3:
            t, x, y = outputs[n]
            queues[t].append((x, y))
            outputs[n] = []


code = intcode.parse_input("23.txt")

vms, input_queues, outputs, flags = create_system(code)
while not input_queues[255]:
    cycle_vms(vms, input_queues, outputs, flags)

x, y = input_queues[255].pop()
print y

vms, input_queues, outputs, flags = create_system(code)
input_queues[255] = []
nat_values = set()
nat_value = None
while nat_value not in nat_values:
    if nat_value is not None:
        nat_values.add(nat_value)
    while any(flags) or not input_queues[255]:
        cycle_vms(vms, input_queues, outputs, flags)
    nat_value = input_queues[255][-1]
    input_queues[255] = []
    input_queues[0].append(nat_value)
    print nat_value
print nat_value[1]
