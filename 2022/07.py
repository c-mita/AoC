import collections

ShCommand = collections.namedtuple("ShCommand", ["cmd", "output"])

def parse_file(filename):
    commands = []
    cmd, output = None, None
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line[0] == "$":
                if cmd:
                    commands.append(ShCommand(cmd, output))
                cmd = line[2:]
                output = []
            else:
                output.append(line)
    if cmd:
        commands.append(ShCommand(cmd, output))
    return commands


class FileNode:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class DirNode:
    def __init__(self, name, parent=None):
        self.name = name
        self.files = {}
        self.children = {}
        self.parent = parent

    def add(self, child):
        if type(child) == FileNode:
            self.files[child.name] = child
        else:
            self.children[child.name] = child


def process_commands(commands):
    root = DirNode("/")
    current = root
    for cmd, output in commands:
        if cmd == "ls":
            for line in output:
                if line.startswith("dir"):
                    d = DirNode(line.split()[1], current)
                    current.add(d)
                else:
                    size, name = line.split()
                    current.add(FileNode(name, int(size)))
        elif cmd.startswith("cd"):
            name = cmd.split()[1]
            if name == "..":
                current = current.parent
            elif name == "/":
                current = root
            else:
                current = current.children[name]
    return root


def find_small_dirs(node, results):
    s = sum(f.size for f in node.files.values())
    for child in node.children.values():
        s += find_small_dirs(child, results)
    if s <= 100000:
        results.append((s, node))
    return s

def get_sizes(node):
    s = sum(f.size for f in node.files.values())
    sizes = {}
    for child in node.children.values():
        c, other_sizes = get_sizes(child)
        s += c
        sizes.update(other_sizes)
    sizes[node] = s
    return s, sizes

commands = parse_file("07_input.txt")
root = process_commands(commands)

results = []
find_small_dirs(root, results)
print(sum(s for (s, n) in results))

total_space = 70000000
required_free = 30000000

total_used, sizes = get_sizes(root)
available = total_space - total_used
to_free = required_free - available

print(min(s for s in sizes.values() if s > to_free))
