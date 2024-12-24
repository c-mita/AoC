def parse_file(filename):
    target_names = {}
    graph = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ":" in line:
                t, v = line.split(": ")
                graph[t] = ["in_%s" % t]
            else:
                n1, op, n2, _, tgt = line.split()
                op_node = "%s_%s" % (op, tgt)
                graph[tgt] = [op_node]
                graph[op_node] = [n1, n2]
        return graph


def dot_data(graph):
    for src, targets in graph.items():
        target_string = ", ".join(targets)
        yield "%s ->{%s};\n" % (src, target_string)


graph = parse_file("24.txt")
with open("24.dot", "w") as f:
    f.write("digraph {\n")
    f.writelines("  " + line for line in dot_data(graph))
    f.write("}\n")
