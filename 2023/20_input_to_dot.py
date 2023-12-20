def parse_file(filename):
    target_names = {}
    graph = {}
    with open(filename) as f:
        for line in f:
            src, targets = line.strip().split(" -> ")
            if src[0] == "%":
                name = "flip_" + src[1:]
                target_names[src[1:]] = name
            elif src[0] == "&":
                name = "conj_" + src[1:]
                target_names[src[1:]] = name
            else:
                name = src
                target_names[src] = name
            graph[name] = targets.split(", ")
    for src in graph:
        graph[src] = [
                target_names[t] if t in target_names else t for t in graph[src]
        ]
    return graph


def dot_data(graph):
    for src, targets in graph.items():
        target_string = ", ".join(targets)
        yield "%s -> {%s};\n" % (src, target_string)

graph = parse_file("20.txt")
with open("20.dot", "w") as f:
    f.write("digraph {\n")
    f.writelines("  " + line for line in dot_data(graph))
    f.write("}\n")

