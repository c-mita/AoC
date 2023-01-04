"""
Not a very conceptually difficult problem; a graph traversal with
Dijkstra's algorithm handles it well enough.
The complexity is largely in generating the set of available moves
due to the complexity of the rule set; because this step is not so performant
the solution for part 2 takes a few seconds to run (< 10s on my laptop).
"""

import collections
import heapq


def parse_file(filename):
    state = {}
    with open(filename) as f:
        for r, l in enumerate(f):
            for c, v in enumerate(l.rstrip()):
                if v in "ABCD":
                    state[(r, c)] = v
    return state


class State:
    costs = {"A":1, "B":10, "C":100, "D":1000}
    target_columns = {"A":3, "B":5, "C":7, "D":9}
    bad_columns = list(target_columns.values())
    min_c = 1
    max_c = 11

    def __init__(self, space):
        self.space = space
        self.depth = int(len(space) // 4)
        self.max_r = self.depth + 1
        self.values = tuple(sorted((pod, r, c) for ((r, c), pod) in self.space.items()))

    def __eq__(self, other):
        return self.values == other.values

    def __hash__(self):
        return hash(self.values)

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        items = sorted(self.space.items(), key=lambda x: (x[1], x[0]))
        return "State({" + ", ".join("%s: '%s'" % (pos, pod) for (pos, pod) in items) + "})"

    def is_pod_in_dest(self, pod, pos):
        pr, pc = pos
        if pos[1] != State.target_columns[pod]:
            return False
        # if our pod is blocking someone in our room then it doesn't count as
        # being "in its destination"
        for r in range(pr+1, self.max_r + 1):
            if (r, pc) in self.space and self.space[(r, pc)] != pod:
                return False
        return True

    def pod_is_blocked(self, pos):
        r, c = pos
        for n in range(2, r):
            if (n, c) in self.space:
                return True
        return False

    def row_in_target_or_false(self, pod):
        tc = State.target_columns[pod]
        slot = False
        for r in range(2, self.max_r + 1):
            if (r, tc) in self.space:
                if self.space[(r, tc)] != pod:
                    return False
            else:
                slot = r
        return slot

    def can_move_to_target(self, pod, pos):
        pr, pc = pos
        tc = State.target_columns[pod]
        # check our corridor is not blocked
        if self.pod_is_blocked(pos):
            return False
        # check our target is clear and movable into
        tr = self.row_in_target_or_false(pod)
        if not tr:
            return False
        # check the route between
        hsteps = range(pc+1, tc+1) if tc > pc else range(pc-1, tc-1, -1)
        for hc in hsteps:
            if (1, hc) in self.space:
                return False
        return (tr, tc)

    @staticmethod
    def cost(pod, start, target):
        sr, sc = start
        tr, tc = target
        d = abs(tc - sc)
        d += sr - 1
        d += tr - 1
        return d * State.costs[pod]

    def create_new_state(self, start, target):
        new_space = dict(self.space)
        new_space[target] = new_space[start]
        del new_space[start]
        return State(new_space)

    def moves(self):
        relevant = [(pos, pod) for (pos, pod) in self.space.items() if not self.is_pod_in_dest(pod, pos)]
        for pos, pod in relevant:
            target = self.can_move_to_target(pod, pos)
            if target:
                yield self.create_new_state(pos, target), self.cost(pod, pos, target)
                return
        for pos, pod in relevant:
            # move along the hallway as much as possible
            pr, pc = pos
            if pr == 1:
                continue
            if self.pod_is_blocked(pos):
                continue
            ranges = range(pc, State.max_c+1), range(pc-1, State.min_c-1, -1)
            for r in ranges:
                for c in r:
                    target = (1, c)
                    if target in self.space:
                        break
                    if c not in State.bad_columns:
                        yield self.create_new_state(pos, target), self.cost(pod, pos, target)


def solve(start_state, target_state):
    distances = collections.defaultdict(lambda: 0x7FFFFFFF)
    distances[start_state] = 0
    visited = set()
    relevant = []
    # break ties in heapq because States are not comparable so tuple order
    # fails without the additional counter
    counter = 0

    current = start_state
    while not current == target_state:
        cdistance = distances[current]
        for state, cost in current.moves():
            if state in visited:
                continue
            nd = cdistance + cost
            d = distances[state]
            if nd < d:
                distances[state] = nd
                d = nd
                heapq.heappush(relevant, (d, counter, state))
                counter += 1
        visited.add(current)
        _d, _c, current = heapq.heappop(relevant)
    return distances[target_state]


parsed_state = parse_file("23_input.txt")
start_state = State(parsed_state)

target_state = State({
    (2,3):"A", (3,3):"A",
    (2,5):"B", (3,5):"B",
    (2,7):"C", (3,7):"C",
    (2,9):"D", (3,9):"D",
})

cost = solve(start_state, target_state)
print(cost)

extended_start_state = {}
middle_rows = ["DCBA", "DBAC"]
for r, c in ((2, 3), (2, 5), (2, 7), (2, 9)):
    extended_start_state[(r, c)] = parsed_state[(r, c)]
for n, row in enumerate(middle_rows):
    for c, v in enumerate(row):
        extended_start_state[(n + 3, 2 * c + 3)] = v
for r, c in ((3, 3), (3, 5), (3, 7), (3, 9)):
    extended_start_state[(5, c)] = parsed_state[(3, c)]

extended_start_state = State(extended_start_state)
extended_target_state = State({
    (2,3):"A", (3,3):"A", (4,3):"A", (5,3):"A",
    (2,5):"B", (3,5):"B", (4,5):"B", (5,5):"B",
    (2,7):"C", (3,7):"C", (4,7):"C", (5,7):"C",
    (2,9):"D", (3,9):"D", (4,9):"D", (5,9):"D",
})

cost = solve(extended_start_state, extended_target_state)
print(cost)
