def parse_input(filename):
    with open(filename) as f:
        return f.readlines()[0].strip()


def calc_visited(moves):
    px, py = 0, 0
    visited = {(px, py)}
    for move in moves:
        if move == ">":
            dx, dy = 1, 0
        elif move == "<":
            dx, dy = -1, 0
        elif move == "^":
            dx, dy = 0, -1
        elif move == "v":
            dx, dy = 0, 1
        px, py = px + dx, py + dy
        visited.add((px, py))
    return visited


data = parse_input("03.txt")
visited = calc_visited(data)
print(len(visited))

moves_1 = data[:-1:2]
moves_2 = data[1::2]
visited_1 = calc_visited(moves_1)
visited_2 = calc_visited(moves_2)
print(len(visited_1 | visited_2))
