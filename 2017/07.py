from collections import Counter

def parse_line(line):
    parts = line.strip().split(" -> ")
    node, weight = parts[0].split()
    weight = int(weight.strip("()"))
    children = parts[1].split(", ") if len(parts) > 1 else []
    return node, weight, children

def parse_input(filename):
    weights = {}
    children = {}
    with open(filename) as f:
        for line in f:
            node, weight, childs = parse_line(line)
            weights[node] = weight
            children[node] = childs
    return weights, children

def find_ancestors(structure):
    ancestors = {n:list() for n in structure}
    for (node, children) in structure.items():
        for c in children: ancestors[c].append(node)
    return ancestors

def weigh_up(structure, node_weights, root):
    accumulated_weights = {}
    total_weight = node_weights[root]
    for c in structure[root]:
        weights = weigh_up(structure, node_weights, c)
        total_weight += weights[c]
        accumulated_weights.update(weights)
    accumulated_weights[root] = total_weight
    return accumulated_weights


def find_unbalanced_node(structure, accumulated_weights, root):
    children = structure[root]
    if len(children) == 0: return None
    child_weights = Counter()
    for w in (accumulated_weights[c] for c in children):
        child_weights[w] += 1
    for c in children:
        w = accumulated_weights[c]
        if child_weights[w] == 1:
            unbalanced = find_unbalanced_node(structure, accumulated_weights, c)
            return unbalanced or (c, child_weights)
    return None

weights, children = parse_input("07_input.txt")

"""
weights = {"pbga":66, "xhth":57, "ebii":61, "havc":66,
        "ktlj":57, "fwft":72, "qoyq":66, "padx":45, "tknk":41,
        "jptl":61, "ugml":68, "gyxo":61, "cntj":57}

children = {"fwft":["ktlj", "cntj", "xhth"],
        "padx":["pbga", "havc", "qoyq"],
        "tknk":["ugml", "padx", "fwft"],
        "ugml":["gyxo", "ebii", "jptl"]}

for w in weights:
    if w not in children: children[w] = list()
"""

ancestors = find_ancestors(children)

root = [n for (n, v) in ancestors.items() if len(v) == 0][0]
print root

accumulated_weights = weigh_up(children, weights, root)
unbalanced_node, child_weights = find_unbalanced_node(children, accumulated_weights, root)
print unbalanced_node, child_weights

w1, w2 = child_weights.keys()
if child_weights[w1] < child_weights[w2]:
    req_weight, faulty_weight = w2, w1
else:
    req_weight, faulty_weight = w1, w2
weight_diff = req_weight - faulty_weight
print weights[unbalanced_node] + weight_diff
