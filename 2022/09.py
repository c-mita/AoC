def parse_file(filename):
    with open(filename) as f:
        moves = []
        for line in f:
            direction, value = line.strip().split(" ")
            step = {"U":(-1,0), "D":(1,0), "R":(0,-1), "L":(0,1)}[direction]
            moves.append((step, int(value)))
    return moves


def process_moves(moves, length):
    def process_move(segments, move):
        delta, size = move
        visited = set()
        box = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for n in range(size):
            head = segments[0][0] + delta[0], segments[0][1] + delta[1]
            segments[0] = head
            for k in range(len(segments) - 1):
                h = segments[k]
                s = segments[k + 1]
                neigbours = [(h[0] + x, h[1] + y) for (x, y) in box]
                if s not in neigbours:
                    dx, dy = h[0] - s[0], h[1] - s[1]
                    dx = 1 if dx > 0 else -1 if dx < 0 else 0
                    dy = 1 if dy > 0 else -1 if dy < 0 else 0
                    s = s[0] + dx, s[1] + dy
                segments[k + 1] = s
            visited.add(segments[-1])
        return visited

    segments = [(0,0)] * length
    visited = set()
    for move in moves:
        visited |= process_move(segments, move)
    return visited


moves = parse_file("09_input.txt")

visited = process_moves(moves, 2)
print(len(visited))
visited = process_moves(moves, 10)
print(len(visited))
