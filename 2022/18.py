import re


def parse_file(filename):
    with open(filename) as f:
        return [tuple(map(int, re.findall("-?[0-9]+", line))) for line in f]


def count_connections(cubes):
    """
    Walk graph of neighbouring cubes, counting each connection.
    Each edge is walked twice (once from each side), but that's fine
    because each edge corresponds to two faces.
    """
    def neighbours(cube):
        x, y, z = cube
        yield from (
                (x-1, y, z), (x+1, y, z),
                (x, y-1, z), (x, y+1, z),
                (x, y, z-1), (x, y, z+1),
        )

    visited = set()
    def dfs(start):
        edges = 0
        if start in visited:
            return 0
        to_visit = [start]
        visited.add(start)
        while to_visit:
            cube = to_visit.pop()
            for neighbour in neighbours(cube):
                if neighbour in cubes:
                    edges += 1
                    if neighbour not in visited:
                        to_visit.append(neighbour)
                        visited.add(neighbour)
        return edges

    return sum(dfs(cube) for cube in cubes)


def count_surface_connections(cubes):
    """
    Wrap our cube set in a bounding box and start within this box.
    Making the box just a bit bigger, so it doesn't touch our cube set
    means we can see every cube outside the cube set in a single walk.
    Count how often we touch a cube in our cube set.
    """
    def neighbours(cube):
        x, y, z = cube
        yield from (
                (x-1, y, z), (x+1, y, z),
                (x, y-1, z), (x, y+1, z),
                (x, y, z-1), (x, y, z+1),
        )
    min_x = min(cubes, key=lambda v:v[0])[0]
    max_x = max(cubes, key=lambda v:v[0])[0]
    min_y = min(cubes, key=lambda v:v[1])[1]
    max_y = max(cubes, key=lambda v:v[1])[1]
    min_z = min(cubes, key=lambda v:v[2])[2]
    max_z = max(cubes, key=lambda v:v[2])[2]

    visited = set()
    lx, hx = min_x - 1, max_x + 1
    ly, hy = min_y - 1, max_y + 1
    lz, hz = min_z - 1, max_z + 1

    def dfs(start):
        surfaces = 0
        if start in visited:
            return 0
        to_visit = [start]
        visited.add(start)
        while to_visit:
            cube = to_visit.pop()
            for neighbour in neighbours(cube):
                if neighbour in cubes:
                    surfaces += 1
                    continue
                nx, ny, nz = neighbour
                if lx <= nx <= hx and ly <= ny <= hy and lz <= nz <= hz and neighbour not in visited:
                    to_visit.append(neighbour)
                    visited.add(neighbour)
        return surfaces
    return dfs((lx, ly, lz))

cubes = parse_file("18_input.txt")
big_cube = [(1,1,1), (2,1,1), (1,2,1), (2,2,1), (1,1,2), (2,1,2), (1,2,2), (2,2,2)]
cubes = set(cubes)
connecting_faces = count_connections(cubes)
print(len(cubes) * 6 - connecting_faces)

surface_faces = count_surface_connections(cubes)
print(surface_faces)
