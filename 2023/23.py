"""
Part 1:
Easy, just run a depth-first walk to identify all possible routes through the
"maze" and pick the longest one.

Part 2:
The space is now a little bit too connected with loops.
Reusing the part 1 solution with the looser restriction will be too slow.

Instead identify the "interesting" nodes; points where we have to make a
choice about where to go next (the branching points) or terminal points (where
we can go no further, to identify the start and end points).
Build up a graph of {node:[(next_node, distance)]} and then run a DFS over
this graph to get the longest route.

(Can't be clever with Dijkstra's + negative weights because that doesn't
work :( )

Final optimization is to terminate the search when the target's predecessor
node is reached (the DFS walk will continue exploring dead ends from there).

Runtime ~ 10 seconds.
"""


def parse_file(filename):
    space = {}
    with open(filename) as f:
        for r, line in enumerate(f):
            for c, s in enumerate(line.strip()):
                if s != "#":
                    space[(r, c)] = s
    return space


def icy_steps(pos, space):
    def steps():
        px, py = pos
        s = space[pos]
        if s == ">":
            yield (px, py+1)
        elif s == "<":
            yield (px, py-1)
        elif s == "v":
            yield (px+1, py)
        elif s == "^":
            yield (px-1, py)
        elif s == ".":
            yield (px-1, py)
            yield (px+1, py)
            yield (px, py-1)
            yield (px, py+1)
        else:
            raise ValueError("Bad symbol '%s'" % s)
    for p in steps():
        if p in space:
            yield p, 1


def non_icy_steps(pos, space):
    def steps():
        px, py = pos
        yield (px-1, py)
        yield (px+1, py)
        yield (px, py-1)
        yield (px, py+1)
    for p in steps():
        if p in space:
            yield p, 1


def find_paths(graph, start, target, next_function):
    def dfs():
        visited = set()
        distance = 0
        stack = [(True, start, 0)]
        while stack:
            forward, current, cost = stack.pop()
            if not forward:
                visited.remove(current)
                distance -= cost
                continue
            stack.append((False, current, cost))
            visited.add(current)
            distance += cost
            if current == target:
                yield distance
            else:
                for n, n_cost in next_function(current, graph):
                    if n in visited:
                        continue
                    stack.append((True, n, n_cost))
    return list(dfs())


def next_interesting_nodes(space, start, next_function):
    def walk(current, prev):
        steps = 0
        while True:
            choices = list(n for n, _c in next_function(current, space) if n != prev)
            if len(choices) != 1:
                return current, steps
            prev = current
            current = choices[0]
            steps += 1
    for n, _c in next_function(start, space):
        target, steps = walk(n, start)
        if target == start:
            # should not happen
            continue
        # steps + 1 because we took a step to get to "n"
        yield target, steps + 1


def build_graph(space, start, step_function):
    graph = {}
    to_visit = [start]
    visited = {start}
    while to_visit:
        current = to_visit.pop()
        graph[current] = []
        for node, distance in next_interesting_nodes(space, current, step_function):
            graph[current].append((node, distance))
            if node not in visited:
                visited.add(node)
                to_visit.append(node)
    return graph


space = parse_file("23.txt")
start = min(k for k in space)
target = max(k for k in space)
paths = find_paths(space, start, target, next_function=icy_steps)
print(max(paths))

graph = build_graph(space, start, non_icy_steps)
# because we cannot loop, we can end our seach once we hit the
# predecessor node of the exit (the last time we can make a choice)
# choosing the "wrong" way stops us from ever reching the end, so
# there's no point running the search from there
predecessor, final_length = graph[target][0]
paths = find_paths(graph, start, predecessor, next_function=lambda c, g: g[c])
print(max(paths) + final_length)
