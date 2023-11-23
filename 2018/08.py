from collections import namedtuple

Node = namedtuple("Node", ["n_children", "n_meta", "children", "metadata"])


def parse_input(filename):
    with open(filename) as f:
        data = f.readlines()[0].strip()
    return map(int, data.split())


def evaluate_tree(root):
    if len(root.children) == 0:
        return sum(root.metadata)
    child_idxs = [v-1 for v in root.metadata if 0 < v <= len(root.children)]
    return sum(evaluate_tree(root.children[i]) for i in child_idxs)


def deserialise_tree(data_stream):
    fake_root = Node(1, 0, [], [])
    node_stack = [fake_root]
    meta_entries = []
    while node_stack:
        current_node = node_stack[-1]
        if current_node.n_children == len(current_node.children):
            meta = list(next(data_stream) for n in range(current_node.n_meta))
            meta_entries.extend(meta)
            current_node.metadata.extend(meta)
            node_stack.pop()
            if node_stack:
                node_stack[-1].children.append(current_node)
        else:
            n_children = next(data_stream)
            n_meta = next(data_stream)
            node_stack.append(Node(n_children, n_meta, [], []))
    root = fake_root.children[0]
    return root, meta_entries


TEST_DATA = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]

data = parse_input("08_input.txt")
#data = TEST_DATA

tree_root, meta_entries = deserialise_tree(iter(data))
print(sum(meta_entries))

print(evaluate_tree(tree_root))
