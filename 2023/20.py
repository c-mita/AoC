"""
Oh how to explain this one...

Part 1 is easy; write a routine that follows the instructions to the letter
and calculate the answer.

Part 2 may be "that" problem of the year. It cannot reasonably be solved
for arbitary inputs. But our input is not arbitrary.

The setup is made clearer by passing the input to a graph drawing tool like
graphviz. An additional "20_input_to_dot.py" script will convert the input to
graphviz's DOT format.

This reveals the graph structure to be a set of subgraphs; each being a loop
of "flip" nodes, some of which feed a "conjunction" node.
These conjuction nodes then link up to input into a final conjuction node
which feeds straight into "rx".
The loops reveal themselves to be mere "binary counters". When a certain value
is reached, the "counter" (the loop of flip nodes) resets back to 0 and the
conjuction node sends a "high" pulse.

We identify the counters by looking at the parents of the parent to "rx".
We then run the process until these inputs are activated, tracking how
long it takes to do so. A simple Least-Common-Multiple calculation gives
us the final result.

One tiny wrinkle is that the a counter-loop will reset itself immediately
after sending a high output, sending a low output in the process. This means
that the "conjucion" node _never_ has all items in its memory as "high" after
a button press has resolved.

Not "fast": ~1 second to calculate everything on a laptop.
"""


import collections
import functools


Module = collections.namedtuple("Module", field_names = ["type", "state"])


FLIP_FLOP = "f"
CONJUNCTION = "c"
BROADCAST = "b"


def parse_file(filename):
    graph = {}
    reverse_graph = collections.defaultdict(list)
    with open(filename) as f:
        for line in f:
            src, targets = line.strip().split(" -> ")
            if src == "broadcaster":
                module = Module(type=BROADCAST, state=0)
            elif src[0] == "%":
                module = Module(type=FLIP_FLOP, state=0)
                src = src[1:]
            elif src[0] == "&":
                module = Module(type=CONJUNCTION, state=None)
                src = src[1:]
            else:
                raise ValueError("Bad value %s" % src)
            targets = targets.split(", ")
            graph[src] = (module, targets)
            for target in targets:
                reverse_graph[target].append(src)

    for src in graph:
        module, targets = graph[src]
        if module.type == CONJUNCTION:
            inputs = reverse_graph[src]
            keys = tuple(inputs)
            values = (0,) * len(keys)
            new_module = Module(module.type, state=(keys, values))
            graph[src] = (new_module, targets)

    return graph


def push_button(graph, to_break={}):
    pulse_queue = collections.deque([("button", "broadcaster", 0)])
    high_pulses, low_pulses = 0, 0
    hit_break = []
    while pulse_queue:
        src, node, pulse = pulse_queue.popleft()
        if pulse:
            high_pulses += 1
        else:
            low_pulses += 1
        if node not in graph:
            continue

        module, targets = graph[node]
        to_send = None
        updated_state = module.state

        if module.type == FLIP_FLOP:
            if pulse == 0:
                to_send = 0 if module.state else 1
                updated_state = to_send
        elif module.type == CONJUNCTION:
            keys, memory = module.state
            memory = list(memory)
            memory[keys.index(src)] = pulse
            to_send = 0 if all(memory) else 1
            updated_state = keys, tuple(memory)
        elif module.type == BROADCAST:
            to_send = pulse
        else:
            raise ValueError("Bad type %s" % module.type)

        if node in to_break and to_send == to_break[node]:
            hit_break.append(node)

        graph[node] = Module(type=module.type, state=updated_state), targets
        if to_send != None:
            for target in targets:
                pulse_queue.append((node, target, to_send))

    if to_break:
        return hit_break
    return high_pulses, low_pulses


def run_machine(graph, steps=20000):
    high, low = 0, 0
    graph = dict(graph)
    for _ in range(steps):
        h, l = push_button(graph)
        high += h
        low += l
    return high, low


def gcd(a, b):
    if a < b:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a % b)


def lcm(a, b):
    return int(a * b / gcd(a, b))


def solve_for_rx(graph):
    reverse_graph = collections.defaultdict(list)
    for src, (module, targets) in graph.items():
        for target in targets:
            reverse_graph[target].append(src)
    if len(reverse_graph["rx"]) != 1:
        raise ValueError("Expected only one input to rx")
    rx_input = reverse_graph["rx"][0]
    module, _ = graph[rx_input]
    if module.type != CONJUNCTION:
        raise ValueError("Expecting conjuction, got %s" % module.type)

    # we track the "break on (node, signal)" in a dict
    # to avoid having to reset the graph and start counting
    # from 0 for each key, which wastes time.
    keys = module.state[0]
    lengths = []
    break_on = {k:1 for k in keys}
    mutable = dict(graph)
    n = 0
    while break_on:
        n += 1
        broken = push_button(mutable, to_break=break_on)
        if broken:
            lengths.append(n)
        for b in broken:
            del break_on[b]
    return functools.reduce(lcm, lengths)


graph = parse_file("20.txt")

high, low = run_machine(graph)
print(high * low)

pushes = solve_for_rx(graph)
print(pushes)
