def parse_file(filename):
    walls = set()
    targets = {}
    with open(filename) as f:
        x = 0
        for line in f:
            for c, y in zip(line, xrange(len(line.strip()))):
                if c == "#":
                    walls.add((x, y))
                elif c.isdigit():
                    targets[int(c)] = (x, y)
            x += 1
    return walls, targets

def possible_moves(state, walls):
    pos, targets = state[0], state[1:][0]
    x, y = pos
    neighbours = [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]
    neighbours = [n for n in neighbours if n not in walls]
    moves = []
    for n in neighbours:
        new_targets = targets
        if n in new_targets:
            new_targets = list(new_targets)
            new_targets.remove(n)
            new_targets = tuple(new_targets)
        new_state = (n, new_targets)
        moves.append(new_state)
    return moves

def bfs(start, walls, target=None):
    states = set()
    state = start
    moves = possible_moves(state, walls)
    counts = [1] * len(moves)
    while moves:
        state = moves.pop(0)
        move_count = counts.pop(0)
        if target is not None and state == target:
            return move_count
        elif target is None and len(state[1]) == 0:
            return move_count
        else:
            next_states = [s for s in possible_moves(state, walls) if s not in states]
            moves.extend(next_states)
            states.update(next_states)
            counts.extend([move_count + 1] * len(next_states))
    return None

walls, targets = parse_file("24.txt")
pos = targets[0]
targets = tuple((v[1] for v in targets.items() if v[0] is not 0))
#print pos, targets

#print possible_moves((pos, targets), walls)
print bfs((pos, targets), walls)
final_state = (pos, ())
print bfs((pos, targets), walls, final_state)
