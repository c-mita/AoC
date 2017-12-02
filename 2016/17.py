import hashlib
import time

"""
Grid is 4x4 with upper-right == (0, 0), target at (3, 3)
Perform Depth-first Search to find possible paths
(BFS and DFS have similar performance for this problem)
"""
UP = ("U", (0,-1))
DOWN = ("D", (0, 1))
LEFT = ("L", (-1, 0))
RIGHT = ("R", (1, 0))

def next_moves(current_path, key):
    p = "".join(m[0] for m in current_path)
    h = hashlib.md5("%s%s" % (key, p)).hexdigest()
    moves = []
    valid = "bcdef"
    if h[0] in valid: moves.append(UP)
    if h[1] in valid: moves.append(DOWN)
    if h[2] in valid: moves.append(LEFT)
    if h[3] in valid: moves.append(RIGHT)
    return moves

def dfs(start, target, key, min_only=True):
    solutions = []
    moves = next_moves([], key)
    #positions = [p for p in positions if 0 <= p[0] < 4 and 0 <= p[1] < 4]
    moves = [m for m in moves if
        0 <= start[0] + m[1][0] < 4 and 0 <= start[1] + m[1][1] < 4]
    positions = [(start[0] + m[1][0], start[1] + m[1][1]) for m in moves]
    moves = [[m] for m in moves]
    max_soln = None
    while moves:
        if len(moves) != len(positions):
            raise ValueError("WAIT WHAT?")
        path = moves.pop()
        pos = positions.pop()
        if min_only and max_soln is not None and len(path) > max_soln:
            continue
        if pos == target:
            max_soln = len(path)
            solutions.append(path)
            continue
        steps = next_moves(path, key)
        steps = [m for m in steps if
            0 <= pos[0] + m[1][0] < 4 and 0 <= pos[1] + m[1][1] < 4]
        next_pos = [(pos[0] + m[1][0], pos[1] + m[1][1]) for m in steps]
        next_paths = [path + [m] for m in steps]
        positions.extend(next_pos)
        moves.extend(next_paths)
    solutions = ["".join(m[0] for m in p) for p in solutions]
    solutions.sort(key=len)
    return solutions

st = time.time()
start = (0,0)
target = (3,3)
key = "vwbaicqe"
solutions = dfs(start, target, key, False)
print time.time() - st
print solutions[0]
print len(solutions[-1])
