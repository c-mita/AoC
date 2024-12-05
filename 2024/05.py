"""
Good old directed graphs.

Part 1 is simple; just that elements are in order w.r.t. to the
relevant subgraph.

Part 2 is slightly more complex.
We actually aren't promised that the full input graph is a DAG (it's
actually cyclic), but the subgraph for a given "update" line is a DAG.

It's not clear in general if a topological ordering for a given update
is unique, but we'll assume it is and not worry too much about how we
get there (does the graph induce a total order or just a partial one?).

We calculate the transitive closure of the relevant subgraph and use that
to generate a comparison function, which we can then pass to "sorted()"
(via functools.cmp_to_key because Python3 is weird like that).

We could implement a proper topological sort algorithm, but I don't want to.
"""

import collections
import functools


def parse_file(filename):
    with open(filename) as f:
        rules = collections.defaultdict(list)
        updates = []

        for line in f:
            line = line.strip()
            if not line:
                continue
            elif "|" in line:
                l, r = map(int, line.split("|"))
                rules[l].append(r)
            else:
                updates.append(list(map(int, line.split(","))))
    return rules, updates


def verify_update(update, rules):
    positions = {v:n for n, v in enumerate(update)}
    for p in positions:
        for after in rules[p]:
            if after not in positions:
                continue
            if positions[after] < positions[p]:
                return False
    return True


def transitive_closure(graph):
    closure = {}

    def dfs(v):
        if v in closure:
            return set()
        closure[v] = set()
        for w in graph[v]:
            if w not in graph:
                continue
            closure[v].add(w)
            closure[v] |= dfs(w)
        return closure[v]

    for v in graph:
        dfs(v)
    return closure


def cmp_func(closure):
    def cmp(left, right):
        if left == right:
            return 0
        elif right in closure[left]:
            return -1
        elif left in closure[right]:
            return 1
    return cmp


rules, updates = parse_file("05.txt")

bad_updates = []
s = 0
for update in updates:
    if verify_update(update, rules):
        s += update[len(update) // 2]
    else:
        bad_updates.append(update)
print(s)


s = 0
for update in bad_updates:
    subgraph = {g:rules[g] for g in update}
    closure = transitive_closure(subgraph)
    fixed = sorted(update, key=functools.cmp_to_key(cmp_func(closure)))
    s += fixed[len(fixed) // 2]
print(s)
