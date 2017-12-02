from sets import ImmutableSet

# Record state has a collection of (generator, chip) pairs,
# recording only the level somthing is on.

# There is no difference between ((1, 0), (2, 2)) and ((2, 2), (1, 0))
# as far as path finding is concerned

start = (
(0, 0), (0, 1), (0, 1), (2, 2), (2, 2)
)

start2 = (
(0, 0), (0, 0), (0, 0), (0, 1), (0, 1), (2, 2), (2, 2)
)

target = (
(3, 3), (3, 3), (3, 3), (3, 3), (3, 3)
)

target2 = (
(3, 3), (3, 3), (3, 3), (3, 3), (3, 3), (3, 3), (3, 3)
)

FLOORS = 4

def is_valid(distribution):
    cf = {}
    gf = {}
    i = 0
    for g, c in distribution:
        gf[g] = gf.get(g, 0) | 1 << i
        cf[c] = cf.get(c, 0) | 1 << i
        i += 1
    for i in xrange(FLOORS):
        g = gf.setdefault(i, 0)
        c = cf.setdefault(i, 0)
        if g > 0 and (g & c != c):
            return False
    return True

def possible_moves(current):
    next_states = set()
    cf, gf = {}, {}
    dist, elev = current
    for (g, c), i in zip(dist, range(len(dist))):
        gf[g] = gf.get(g, 0) | 1 << i
        cf[c] = cf.get(c, 0) | 1 << i
        i += 1
    #we can move one thing up or down or two things up or down
    for floor_delta in [-1, 1]:
        if elev + floor_delta < 0 or elev + floor_delta > FLOORS - 1:
            continue
        flattened = list((v for p in dist for v in p))
        for v1, i in zip(flattened, xrange(len(flattened))):
            # move only one item
            if v1 == elev:
                new_flat = list(flattened)
                new_flat[i] += floor_delta
                new_dist = tuple( (new_flat[x], new_flat[x+1])
                        for x in xrange(0, len(new_flat), 2) )
                next_states.add((new_dist, elev + floor_delta))
                for j in xrange(i + 1, len(flattened)):
                    v2 = flattened[j]
                    if v2 == elev:
                        new_flat2 = list(new_flat)
                        new_flat2[j] += floor_delta
                        new_dist = tuple( (new_flat2[x], new_flat2[x+1])
                                for x in xrange(0, len(new_flat2), 2) )
                        next_states.add((new_dist, elev + floor_delta))
    return [s for s in next_states if is_valid(s[0])]

def bfs(start, target):
    states = set()
    state = start
    moves = possible_moves(state)
    counts = [1] * len(moves)
    while moves:
        state = moves.pop(0)
        move_count = counts.pop(0)
        if state == target:
            return move_count
        else:
            # since the "order" of pairs doesn't matter, we can sort to
            # increase the chances of eliminating branches
            next_states = [(tuple(sorted(s[0])), s[1]) for s in possible_moves(state)]
            next_states = [s for s in next_states if s not in states]
            moves.extend(next_states)
            states.update(next_states)
            counts.extend([move_count + 1] * len(next_states))
    raise ValueError("NOT FOUND")

print bfs((start, 0), (target, 3))
print bfs((start2, 0), (target2, 3))
