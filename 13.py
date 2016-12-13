def bit_sum(n):
    s = 0
    while n > 0:
        s += n & 1
        n >>= 1
    return s

def is_open(pos, key):
    x, y = pos
    v = x*x + 3*x + 2*x*y + y + y*y
    v += key
    return bit_sum(v) & 1 == 0

def possible_steps(pos, key):
    x, y = pos
    steps = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    steps = [s for s in steps if is_open(s, key) and s[0] >= 0 and s[1] >= 0]
    return steps

def bfs(start, target, key):
    visited = set()
    pos = start
    moves = possible_steps(pos, key)
    counts = [1] * len(moves)
    while moves:
        pos = moves.pop(0)
        move_count = counts.pop(0)
        if pos == target:
            return move_count
        else:
            next_pos = [s for s in possible_steps(pos, key) if s not in visited]
            moves.extend(next_pos)
            visited.update(next_pos)
            counts.extend([move_count + 1] * len(next_pos))
    return None


key = 1362
print bfs((1, 1), (31, 39), key)

def bfs_count(start, max_dist, key):
    visited = set()
    pos = start
    moves = possible_steps(pos, key)
    counts = [1] * len(moves)
    move_count = 0
    while move_count < max_dist:
        pos = moves.pop(0)
        move_count = counts.pop(0)
        next_pos = [s for s in possible_steps(pos, key) if s not in visited]
        moves.extend(next_pos)
        visited.update(next_pos)
        counts.extend([move_count + 1] * len(next_pos))
    return len(visited)

#s = 0
#for x in xrange(0, 52):
#    for y in xrange(0, 52 - x):
#        d = bfs((1, 1), (x, y), key)
#        if d is not None and d <= 50:
#            s += 1
#print s
print bfs_count((1, 1), 50, key)
