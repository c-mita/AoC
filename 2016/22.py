import re

def parse_node(line):
    name, size, used, avail, usep = line.split()
    size = int(re.findall("[0-9]+", size)[0])
    used = int(re.findall("[0-9]+", used)[0])
    avail = int(re.findall("[0-9]+", avail)[0])
    x = int(re.findall("x[0-9]+", name)[0][1:])
    y = int(re.findall("y[0-9]+", name)[0][1:])
    return ((x, y), size, used, avail)

def parse_file(filename):
    with open(filename) as f:
        lines = [line for line in f]
        return [parse_node(line) for line in lines[2:]]

#test_line = "/dev/grid/node-x20-y05     91T   71T    20T   78%"
#print parse_node(test_line)

def count_viable_pairs(nodes):
    c = 0
    for n1 in nodes:
        for n2 in nodes:
            if n1 is n2: continue
            if n1[2] > 0 and n2[3] >= n1[2]:
                c += 1
    return c

def produce_state(nodes):
    x = 0
    i = 0
    state = []
    while i < len(nodes):
        state.append([])
        while nodes[i][0][0] == x:
            state[x].append(nodes[i][1:])
            i += 1
            if i >= len(nodes): break
        state[x] = tuple(state[x])
        x += 1
    return tuple(state)

def possible_moves(state):
    pos, grid = state
    next_states = []
    for x in xrange(len(grid)):
        for y in xrange(len(grid[x])):
            node = grid[x][y]
            neighbours = [(x-1, y-1), (x-1, y), (x-1, y+1),
                    (x, y-1), (x, y+1),
                    (x+1, y-1), (x+1, y), (x+1, y+1)]
            neighbours = [(x2, y2) for (x2, y2) in neighbours if
                    0 <= x2 < len(grid) and 0 <= y2 < len(grid[x])]
            for x2, y2 in neighbours:
                pos2 = (x2, y2) if (x, y) == pos else (x, y)
                node2 = grid[x2][y2]
                if node2[2] >= node[1]:
                    g2 = list(grid)
                    g2[x2] = list(g2[x2])
                    g2[x2][y2] = list(g2[x2][y2])
                    g2[x2][y2][1] += g2[x][y][1]
                    g2[x2][y2][2] -= g2[x][y][1]
                    g2[x2][y2] = tuple(g2[x2][y2])
                    g2[x2] = tuple(g2[x2])
                    g2[x] = list(g2[x])
                    g2[x][y] = list(g2[x][y])
                    g2[x][y][1] = 0
                    g2[x][y][2] = g2[x][y][0]
                    g2[x][y] = tuple(g2[x][y])
                    g2[x] = tuple(g2[x])
                    next_states.append((pos2, tuple(g2)))
    return next_states

nodes = parse_file("22.txt")
print count_viable_pairs(nodes)
grid = produce_state(nodes)

start_pos = (len(grid)-1, 0)
target_pos = (0, 0)

def produce_map(state):
    pos, grid = state
    output = ""
    for x in xrange(len(grid)):
        line = []
        for y in xrange(len(grid[x])):
            node = grid[x][y]
            symbol = "."
            if (x, y) == pos: symbol = "D"
            if (x, y) == (0, 0): symbol = "E"
            if node[1] == 0: symbol = "_"
            if node[1] > 85: symbol = "#"
            line.append("%s " % symbol)
        line.append(" %d" % x)
        output += "".join(line) + "\n"
    output += "".join(["%d " % (y % 10) for y in xrange(len(grid[0]))])
    return output

print produce_map((start_pos, grid))
