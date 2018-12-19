TEST_INPUT = [['C', 'A'], ['C', 'F'], ['A', 'B'], ['A', 'D'], ['B', 'E'], ['D', 'E'], ['F', 'E']]

with open("07_input.txt") as f:
    instructions = [(l[5], l[36]) for l in f.readlines()]


nodes = set(c[0] for c in instructions)
nodes.update(c[1] for c in instructions)

graph = {step:[] for step in nodes}
rev_graph = {step:[] for step in nodes}
for (dep, node) in instructions:
    graph[node].append(dep)
    rev_graph[dep].append(node)

for k in graph:
    graph[k] = sorted(graph[k])

import copy
proc_graph = copy.deepcopy(graph)

linear_steps = []
while proc_graph:
    candidates = [k for (k, v) in proc_graph.iteritems() if not v]
    step = sorted(candidates)[0]
    linear_steps.append(step)
    del proc_graph[step]
    for s in rev_graph[step]:
        proc_graph[s].remove(step)

print "".join(linear_steps)


proc_graph = copy.deepcopy(graph)
n_workers = 5
step_time_base = 60

n_running = 0
running = set()
time = 0
while proc_graph:
    # add all candidate jobs to the running set (subject to worker constraint)
    candidates = [k for (k, v) in proc_graph.iteritems() if not v]
    for step in sorted(candidates):
        if len(running) >= 5:
            break
        del proc_graph[step]
        running.add((step, time + step_time_base + ord(step) - 0x40))

    # remove the first to complete job
    (completed, complete_time) = min(running, key=lambda (step, time): time)
    running.remove((completed, complete_time))
    time = complete_time
    # remove completed job from dependency list
    for s in rev_graph[completed]:
        proc_graph[s].remove(completed)


if running:
    complete_time = max(running, key=lambda (step, time): time)
else:
    complete_time = time
print complete_time
