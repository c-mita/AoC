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

def find_empty(nodes):
    empties = []
    for node in nodes:
        if node[2] == 0:
            empties.append(node)
    return empties

def produce_simplified_grid(nodes, empty):
    grid = {}
    for node in nodes:
        if node[2] > empty[1]: grid[node[0]] = -1
        elif node[2] == 0: grid[node[0]] = 0
        else: grid[node[0]] = 1
    return grid

def find_walls(nodes, empty):
    walls = set()
    for node in nodes:
        if node[2] > empty[1]: walls.add(node[0])
    return walls

def find_bounds(nodes):
    x, y = 0, 0
    for node in nodes:
        x, y = max(x, node[0][0]), max(y, node[0][1])
    return (x+1, y+1)

def possible_moves(state, walls, bounds):
    empty, data = state
    ex, ey = empty
    neighbours = [(ex-1, ey), (ex, ey-1), (ex, ey+1), (ex+1, ey)]
    neighbours = [n for n in neighbours if n not in walls]
    neighbours = [(x, y) for (x, y) in neighbours if
            0 <= x < bounds[0] and 0 <= y < bounds[1]]
    data = [tuple(empty) if n == data else tuple(data) for n in neighbours]
    return [(e, d) for (e, d) in zip(neighbours, data)]

def bfs(empty, data, data_target, walls, bounds):
    print empty, data, data_target, bounds
    states = set()
    state = (empty, data)
    moves = possible_moves(state, walls, bounds)
    counts = [1] * len(moves)
    while moves:
        state = moves.pop(0)
        move_count = counts.pop(0)
        if state[1] == data_target:
            return move_count
        else:
            next_states = [s for s in possible_moves(state, walls, bounds) if s not in states]
            moves.extend(next_states)
            states.update(next_states)
            counts.extend([move_count + 1] * len(next_states))
    return None


nodes = parse_file("22.txt")
empty = find_empty(nodes)[0]

bounds = find_bounds(nodes)
print bounds
state = (empty, (11, 10))
walls = find_walls(nodes, empty)

print possible_moves(((32, 0), (33, 0)), walls, bounds)
print bfs(empty[0], (bounds[0]-1, 0), (0, 0), walls, bounds)
