"""
I think the first "hard" problem for me? At least I had to spend more time
thinking about than others, even if the solution is actually realtively
straightforward.

We "assume" that, given two sequences with lengths A and B,
A <= B implies A' <= B' where S' is the command required to generate
sequence S.
This means we only need to track minimums.

We set up a "DP" recursion.
At each level, identify the shortest solutions for generating the
required sequence of button presses.
We simply return the length of the shortest solution.

Part 2 is exactly the same if we memoize the recursive function.
"""


import collections
import functools


KEYPAD = {
    "7": {"v":"4", ">":"8"},
    "8": {"<":"7", "v":"5", ">":"9"},
    "9": {"<":"8", "v":"6"},
    "4": {"v":"1", ">":"5", "^":"7"},
    "5": {"<":"4", "v":"2", ">":"6", "^":"8"},
    "6": {"<":"5", "v":"3", "^":"9"},
    "1": {">":"2", "^":"4"},
    "2": {"<":"1", "v":"0", ">":"3", "^":"5"},
    "3": {"<":"2", "v":"A", "^":"6"},
    "0": {">":"A", "^":"2"},
    "A": {"<":"0", "^":"3"},
}

CONTROLS = {
        "A": {"<":"^", "v":">"},
        "^":{"v":"v", ">":"A"},
        "<":{">":"v"},
        "v":{"<":"<", ">":">", "^":"^"},
        ">":{"<":"v", "^":"A"},
}


def routes(start, target, graph):
    paths = []
    queue = collections.deque([(start, "")])
    distance = 0x7FFFFFFF
    while queue:
        path, commands = queue.popleft()
        if len(path) > distance:
            continue
        v = path[-1]
        if v == target:
            distance = len(path)
            paths.append((path, commands))
        for d, t in graph[v].items():
            queue.append((path + t, commands + d))
    return paths


@functools.cache
def solve_keypad(sequence, length):
    if not length:
        return len(sequence)
    graph = KEYPAD
    if ">" in sequence or "<" in sequence or "^" in sequence or "v" in sequence:
        graph = CONTROLS

    # we always start at A because a robot always finishes a sequence
    # by pressing a button, so it's at A the next time it does anything
    sequence = "A" + sequence
    result = 0
    for start, target in zip(sequence[:-1], sequence[1:]):
        paths = []
        for path, command in routes(start, target, graph):
            command = command + "A"
            sub = solve_keypad(command, length-1)
            paths.append(sub)
        result += min(paths)
    return result


def complexity(code, robots=3):
    l = solve_keypad(code, length=robots)
    n = int("".join(c for c in code if c != "A"))
    return l * n


INPUT = """
540A
582A
169A
593A
579A
"""


codes = [l.strip() for l in INPUT.split() if l.strip()]

s = sum(complexity(code, robots=3) for code in codes)
print(s)

s = sum(complexity(code, robots=26) for code in codes)
print(s)

