from collections import defaultdict

"""
A simple BFS over the maze might manage to solve the first part, but part 2
cannot reasonable be solved in that manner.

Find every unique path between each pair of keys (and the start) using a
simple depth-first walk and record the distances with the keys required to
walk that path.

With this, we use Dijkstra's Algorithm to find the shortest path that obtains
every key (the graph is represented by (position, keys_found) and the target
is the first node we visit that has all keys).

Part 2 is fundamentally the same, we really just have four positions in our
graph position tuple, so a node in our graph is represented by something like:
(pos_1, pos_2, pos_3, pos_4, keys_found)
"""

class Maze:

    _KEYS = "abcdefghijklmnopqrstuvwxyz"
    _DOORS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, maze):
        self.maze = maze
        self.distance_cache = {}
        self.locations = {}

        self.keys = ""
        self.doors = ""
        for v in maze.values():
            if v in self._DOORS:
                self.doors += v
            if v in self._KEYS:
                self.keys += v
        self.keys = "".join(sorted(self.keys))
        self.doors = "".join(sorted(self.doors))

        for k, v in maze.items():
            if v in self.keys + "@":
                self.locations[v] = k
        self.start = self.locations["@"]

        self.paths = {}
        for start in self.keys + "@":
            self.paths[start] = self._find_paths(self.locations[start])


    def __getitem__(self, key):
        return self.maze[key]


    def get_neighbours(self, position, keys):
        px, py = position
        neighbours = set()
        for nx, ny in [(px-1, py), (px+1, py), (px, py-1), (px, py+1)]:
            c = self.maze[(nx, ny)] if (nx, ny) in self.maze else "#"
            if c == "." or c == "@" or c in self._KEYS:
                neighbours.add((nx, ny))
            elif c in self._DOORS and c.lower() in keys:
                neighbours.add((nx, ny))
        return neighbours


    def get_paths(self, start, keys):
        options = {}
        for target, routes in self.paths[self.maze[start]].items():
            if target in keys:
                continue
            to_target = []
            for rkeys, distance in routes.items():
                if all(c in keys for c in rkeys):
                    to_target.append(distance)
            if to_target:
                options[target] = min(to_target)
        return options


    def _find_paths(self, start):
        # perform DFS to find all paths from start to other nodes
        visited = set()
        distance = 0
        paths = defaultdict(dict)

        def dfs(node, keys, visited, paths):
            value = self.maze[node]
            if value in self._KEYS:
                if keys in paths[value]:
                    if paths[value][keys] <= len(visited):
                        return
                paths[value][keys] = len(visited)

            visited.add(node)
            n_keys = keys
            # passing over a key counts as "requiring" it, since we want to
            # ensure our code records picking it up when stepping over it,
            # otherwise it would have to revist it later.
            if value in self._DOORS or value in self._KEYS:
                n_keys = "".join(sorted(keys + value.lower()))
            for n_node in self.get_neighbours(node, self._KEYS):
                if n_node in visited: continue
                dfs(n_node, n_keys, visited, paths)
            visited.remove(node)

        dfs(start, "", visited, paths)
        return paths


def parse_input(filename):
    maze = {}
    with open(filename) as f:
        for j, l in enumerate(f):
            for i, c in enumerate(l):
                maze[(j, i)] = c
    return maze


def parse_split_maze(filename):
    maze = parse_input(filename)
    start = (k for k, v in maze.items() if v == "@").next()
    sx, sy = start
    # assumes the boundary of the separated mazes is an axis-aligned cross
    maze[(sx, sy)], maze[(sx-1, sy)], maze[(sx+1, sy)] = "#", "#", "#"
    maze[(sx, sy-1)], maze[(sx, sy+1)] = "#", "#"
    maze[(sx-1, sy-1)] = "@"
    maze[(sx+1, sy-1)] = "@"
    maze[(sx-1, sy+1)] = "@"
    maze[(sx+1, sy+1)] = "@"
    maze_1 = {(x,y):v for (x, y), v in maze.items() if x <= sx and y <= sy}
    maze_2 = {(x,y):v for (x, y), v in maze.items() if sx <= x and y <= sy}
    maze_3 = {(x,y):v for (x, y), v in maze.items() if x <= sx and sy <= y}
    maze_4 = {(x,y):v for (x, y), v in maze.items() if sx <= x and sy <= y}
    return maze_1, maze_2, maze_3, maze_4


def solve_maze(maze):
    start_pos = maze.start
    start_keys = ""
    distances = defaultdict(lambda: 0x7FFFFFFF)
    distances[(start_pos, start_keys)] = 0
    parents = {}
    relevant_nodes = set([(start_pos, start_keys)])
    visited = set()

    current_node = (start_pos, start_keys)
    while current_node[1] != maze.keys:
        cpos, ckeys = current_node
        cdistance = distances[current_node]
        to_visit = maze.get_paths(cpos, ckeys)
        for tkey, tdistance in to_visit.items():
            tkeys = "".join(sorted(ckeys + tkey))
            tpos = maze.locations[tkey]
            if (tpos, tkeys) not in visited:
                relevant_nodes.add((tpos, tkeys))
            nd = cdistance + tdistance
            if nd < distances[(tpos, tkeys)]:
                distances[(tpos, tkeys)] = nd
        visited.add(current_node)
        relevant_nodes.remove(current_node)
        current_node = min(relevant_nodes, key=lambda k: distances[k])
    return distances[current_node]


def solve_mazes(mazes):
    def next_nodes(positions, keys):
        # possible paths to explore
        to_visit = []
        for n, (maze, pos) in enumerate(zip(mazes, positions)):
            options = maze.get_paths(pos, keys)
            for tkey, tdistance in options.items():
                tpos = maze.locations[tkey]
                new_positions = positions[:n] + (tpos,) + positions[n+1:]
                new_keys = "".join(sorted(keys + tkey))
                to_visit.append((new_positions, new_keys, tdistance))
        return to_visit

    start_pos = tuple(maze.start for maze in mazes)
    start_keys = ""
    target_keys = "".join(sorted(set("".join(maze.keys for maze in mazes))))
    distances = defaultdict(lambda: 0x7FFFFFFF)
    distances[(start_pos, start_keys)] = 0
    visited = set()
    relevant_nodes = set([(start_pos, start_keys)])

    current_node = (start_pos, start_keys)
    while current_node[1] != target_keys:
        cpos, ckeys = current_node
        cdistance = distances[current_node]
        to_visit = next_nodes(cpos, ckeys)
        for tpos, tkeys, tdistance in to_visit:
            if (tpos, tkeys) not in visited:
                relevant_nodes.add((tpos, tkeys))
            nd = cdistance + tdistance
            if nd < distances[(tpos, tkeys)]:
                    distances[(tpos, tkeys)] = nd
        visited.add(current_node)
        relevant_nodes.remove(current_node)
        current_node = min(relevant_nodes, key=lambda k:distances[k])
    return distances[current_node]


maze = Maze(parse_input("18_input.txt"))
start = maze.start
distance = solve_maze(maze)
print distance

maze_1, maze_2, maze_3, maze_4 = parse_split_maze("18_input.txt")
maze_1, maze_2, maze_3, maze_4 = Maze(maze_1), Maze(maze_2), Maze(maze_3), Maze(maze_4)

distance = solve_mazes([maze_1, maze_2, maze_3, maze_4])
print distance
