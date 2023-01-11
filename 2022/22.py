import itertools
import re


"""
This was probably my least favourite AOC problem ever, at least in terms of
coding. The problem is actually pretty straightforward conceptually, but
requires just a ton of code to get through.

Part 1 is easy: Just walk around the map, noting that sometimes we have to
look backwards to work out where we end up when we walk off the edge.

Part 2...
The "intended" approach seems to be to manually work out how the input cube
you've been given folds, construct the edge identities yourself, and then
proceed with the walk.

But I am a Professional Software Engineer. Out of sheer bloody mindedness, I
will solve this for the general case.

First the individual segments need to be identified (regions corresponding to
the separate faces of the cube), and walked. For each, we build up the
affine linear transformation that will map them to the faces of a cube in 3D
space.
We need to map our faces so there is no overlap, but that they do "touch" at
corners (to simplify the walk).

Our map is designed so that the faces, for a "4x4 cube", have the following
coordinate bounds (starting segement is mapped to the bottom):

Bottom face:
(1, 1, 0), (1, 4, 0)
(4, 1, 0), (4, 4, 0)

North face:
(0, 1, 1), (0, 4, 1)
(0, 1, 4), (0, 4, 4)

South face:
(5, 1, 1), (5, 4, 1)
(5, 1, 4), (5, 4, 4)

West face:
(1, 0, 1), (1, 0, 4)
(4, 0, 1), (4, 0, 4)

East face:
(1, 5, 1), (1, 5, 4)
(4, 5, 1), (4, 5, 4)

Top face:
(1, 1, 5), (1, 4, 5)
(4, 1, 5), (4, 4, 5)

The walk is relatively straightforward; we need to track our orientation
(which way left is) as well as our direction and position.

Calculating the initial size of the grid is another matter.
There are only 11 topologically unique nets for a cube.
All of them, except one, have a width of 3 times the width of the cube
across the most narrow dimension.
The exception is 2 x 5, and the net looks like this:
    1 2 3
        4 5 6

We can check if our bounds are proportional to this net; if they are, then
we can give the size by simple division by 2, otherwise by 3.

Unusually, we'll use the 1-based indices throughout for this problem.
"""

def parse_file(filename):
    grid = {}
    with open(filename) as f:
        for r, line in enumerate(f):
            if not line.strip("\n"):
                break
            for c, v in enumerate(line.strip("\n")):
                if v == " ":
                    continue
                grid[(r+1, c+1)] = v
        instructions = []
        for instruction in re.findall("[0-9]+|[A-Z]", next(f)):
            if instruction in "LR":
                instructions.append(instruction)
            else:
                instructions.append(int(instruction))
    return grid, instructions


"""
Part 1 comes first, because there's so much code for Part 2.
"""

def create_graph(grid):
    graph = {}
    for (cx, cy) in ((x, y) for ((x, y), v) in grid.items() if v == "."):
        neighbours = {}
        lx = cx - 1
        rx = cx + 1
        uy = cy - 1
        dy = cy + 1
        if (lx, cy) not in grid:
            x = cx
            while ((x + 1), cy) in grid:
                x += 1
            lx = x
        if (rx, cy) not in grid:
            x = cx
            while ((x - 1), cy) in grid:
                x -= 1
            rx = x
        if (cx, uy) not in grid:
            y = cy
            while (cx, (y + 1)) in grid:
                y += 1
            uy = y
        if (cx, dy) not in grid:
            y = cy
            while (cx, (y - 1)) in grid:
                y -= 1
            dy = y
        if (lx, cy) in grid and grid[(lx, cy)] == ".":
            neighbours[(-1, 0)] = (lx, cy)
        if (rx, cy) in grid and grid[(rx, cy)] == ".":
            neighbours[(1, 0)] = (rx, cy)
        if (cx, uy) in grid and grid[(cx, uy)] == ".":
            neighbours[(0, -1)] = (cx, uy)
        if (cx, dy) in grid and grid[(cx, dy)] == ".":
            neighbours[(0, 1)] = (cx, dy)
        graph[(cx, cy)] = neighbours
    return graph


def run_instructions(graph, instructions, start_pos, start_dir):
    directions = {
        (0, 1): {"R":(1, 0), "L":(-1, 0)},
        (1, 0): {"R":(0, -1), "L": (0, 1)},
        (0, -1): {"R":(-1, 0), "L":(1, 0)},
        (-1, 0): {"R":(0, 1), "L":(0, -1)}
    }
    delta = start_dir
    pos = start_pos
    for instruction in instructions:
        if type(instruction) == str:
            delta = directions[delta][instruction]
        else:
            for _ in range(instruction):
                if delta in graph[pos]:
                    pos = graph[pos][delta]
                else:
                    break
    return pos, delta


grid, instructions = parse_file("22_input.txt")
graph = create_graph(grid)
start_pos = min((x, y) for (x, y) in grid if x == 1)
start_dir = (0, 1)

final_pos, final_dir = run_instructions(graph, instructions, start_pos, start_dir)
facing_map = {(0, 1): 0, (1, 0): 1, (0, -1): 2, (-1, 0): 3}
print(final_pos[0] * 1000 + final_pos[1] * 4 + facing_map[final_dir])



"""
Part 2 code begins here.
Obviously with some Matrix code, because we need to do linear algebra.
"""


class Matrix:
    def __init__(self, grid):
        self.grid = grid
        self.nrows = max(self.grid)[0] + 1
        self.ncols = max(self.grid, key=lambda v:v[1])[1] + 1

    @staticmethod
    def from_tuples(*rows):
        m = {}
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                m[(r, c)] = v
        return Matrix(m)

    def __mul__(self, other):
        n = {k:other * v for (k, v) in self.grid.items()}
        return Matrix(n)

    def __rmul__(self, other):
        return self * other

    def __matmul__(self, other):
        if self.ncols != other.nrows:
            raise ValueError("Incompatible dimensions")
        result = {}
        for (r, c) in itertools.product(range(self.nrows), range(other.ncols)):
            v = sum(self.grid[(r, n)] * other.grid[(n, c)] for n in range(self.ncols))
            result[(r, c)] = v
        return Matrix(result)

    def apply(self, vector):
        # pretend our vector is actually a column vector
        result = []
        for r in range(self.nrows):
            v = sum(self.grid[(r, n)] * vector[n] for n in range(self.ncols))
            result.append(v)
        return tuple(result)

    def __repr__(self):
        return "Matrix(%s)" % repr(self.grid)

    def __str__(self):
        rows = []
        for r in range(self.nrows):
            rows.append(" ".join(str(self.grid[(r, c)]) for c in range(self.ncols)))
        return "\n".join(rows)


def find_segments(grid, segment_size):
    segments = []
    for x in range(4):
        for y in range(4):
            sx = segment_size * x
            sy = segment_size * y
            if (sx+1, sy+1) in grid:
                segments.append((x, y))
    return segments


def walk_segments(segments, cube_size):
    """Construct the transformations for the segments."""
    rot_r_y = Matrix.from_tuples((0, 0, -1, 0), (0, 1, 0, 0), (1, 0, 0, 0), (0, 0, 0, 1))
    rot_f_y = Matrix.from_tuples((0, 0, 1, 0), (0, 1, 0, 0), (-1, 0, 0, 0), (0, 0, 0, 1))
    rot_r_x = Matrix.from_tuples((1, 0, 0, 0), (0, 0, 1, 0), (0, -1, 0, 0), (0, 0, 0, 1))
    rot_f_x = Matrix.from_tuples((1, 0, 0, 0), (0, 0, -1, 0), (0, 1, 0, 0), (0, 0, 0, 1))

    start = segments[0]
    sx, sy = start[0], start[1]
    identity = Matrix.from_tuples((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    # transformation in map maps an element in a segment to the coordinates on the cube
    transformations = {start:identity}
    to_visit = [(start, identity)]
    while to_visit:
        next_to_visit = []
        for (x, y), trans in to_visit:
            dx, dy = x - sx, y - sy
            up = (x-1, y)
            down = (x+1, y)
            left = (x, y-1)
            right = (x, y+1)
            # each step is a rotation about an axis, followed by a shift to fix up where the face is placed
            if up in segments and up not in transformations:
                # rotation about y of 90 degrees forwards
                offset1 = Matrix.from_tuples((1, 0, 0, cube_size * dx), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
                offset2 = Matrix.from_tuples((1, 0, 0, -cube_size * dx), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
                shift = Matrix.from_tuples((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 1), (0, 0, 0, 1))
                t = trans @ shift @ offset1 @ rot_f_y @ offset2
                transformations[up] = t
                next_to_visit.append((up, t))
            if down in segments and down not in transformations:
                # rotation about y of 90 degrees backwards
                offset1 = Matrix.from_tuples((1, 0, 0, cube_size * (dx+1)), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
                offset2 = Matrix.from_tuples((1, 0, 0, -cube_size * (dx+1)), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
                shift = Matrix.from_tuples((1, 0, 0, 1), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
                t = trans @ shift @ offset1 @ rot_r_y @ offset2
                transformations[down] = t
                next_to_visit.append((down, t))
            if left in segments and left not in transformations:
                # rotation about x of 90 degrees backwards
                offset1 = Matrix.from_tuples((1, 0, 0, 0), (0, 1, 0, cube_size * dy), (0, 0, 1, 0), (0, 0, 0, 1))
                offset2 = Matrix.from_tuples((1, 0, 0, 0), (0, 1, 0, -cube_size * dy), (0, 0, 1, 0), (0, 0, 0, 1))
                shift = Matrix.from_tuples((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 1), (0, 0, 0, 1))
                t = trans @ shift @ offset1 @ rot_r_x @ offset2
                transformations[left] = t
                next_to_visit.append((left, t))
            if right in segments and right not in transformations:
                # rotation about x of 90 degrees forwards
                offset1 = Matrix.from_tuples((1, 0, 0, 0), (0, 1, 0, cube_size * (dy+1)), (0, 0, 1, 0), (0, 0, 0, 1))
                offset2 = Matrix.from_tuples((1, 0, 0, 0), (0, 1, 0, -cube_size * (dy+1)), (0, 0, 1, 0), (0, 0, 0, 1))
                shift = Matrix.from_tuples((1, 0, 0, 0), (0, 1, 0, 1), (0, 0, 1, 0), (0, 0, 0, 1))
                t = trans @ shift @ offset1 @ rot_f_x @ offset2
                transformations[right] = t
                next_to_visit.append((right, t))
        to_visit = next_to_visit
    return transformations, (sx * cube_size, sy * cube_size)


def apply_mapping(grid, size, origin, transformations):
    forward_map = {}
    reverse_map = {}
    ox, oy = origin
    def calc_segment(point):
        px, py = point
        sx = (px - 1) // size
        sy = (py - 1) // size
        return (sx, sy)
    for plane_point in grid:
        segment = calc_segment(plane_point)
        px, py = plane_point[0] - ox, plane_point[1] - oy
        cube_point = transformations[segment].apply((px, py) + (0, 1))
        cube_point = cube_point[:-1]
        if cube_point in reverse_map:
            for v in cube_point:
                if not 0 <= v <= 5:
                    raise ValueError("Bad point")
        forward_map[plane_point] = cube_point
        reverse_map[cube_point] = plane_point
    return forward_map, reverse_map


def run_instructions_cube(cube, instructions, start, cube_to_plane):
    x_offsets = ((1, 0, 0), (-1, 0, 0))
    y_offsets = ((0, 1, 0), (0, -1, 0))
    z_offsets = ((0, 0, 1), (0, 0, -1))
    xyz_offsets = list(
            itertools.chain(
                itertools.product(x_offsets, y_offsets, z_offsets),
                itertools.product(x_offsets, z_offsets, y_offsets),
                itertools.product(y_offsets, x_offsets, z_offsets),
                itertools.product(y_offsets, z_offsets, x_offsets),
                itertools.product(z_offsets, x_offsets, y_offsets),
                itertools.product(z_offsets, y_offsets, x_offsets),
            )
    )
    # a map of (direction, left_dir) to new_direction options
    # for when we step off the cube
    offsets = {}
    for d, l, nd in xyz_offsets:
        if (d, l) not in offsets:
            offsets[(d, l)] = []
        offsets[(d, l)].append(nd)

    rotation_map = {}
    for d, l in itertools.chain(
            itertools.product(x_offsets, y_offsets),
            itertools.product(x_offsets, z_offsets),
            itertools.product(y_offsets, x_offsets),
            itertools.product(y_offsets, z_offsets),
            itertools.product(z_offsets, x_offsets),
            itertools.product(z_offsets, y_offsets)
    ):
        rd = tuple(-v for v in d)
        rl = tuple(-v for v in l)
        rotation_map[(d, l)] = {
            "L":(l, rd),
            "R":(rl, d),
        }


    def run_step(point, direction, lr_axis, count):
        px, py, pz = point
        dx, dy, dz = direction
        lx, ly, lz = lr_axis
        while count:
            count -= 1
            nx, ny, nz = px + dx, py + dy, pz + dz
            ndx, ndy, ndz = dx, dy, dz
            if (nx, ny, nz) not in cube:
                # we've run off the edge of the cube
                choices = offsets[((dx, dy, dz), (lx, ly, lz))]
                for (cx, cy, cz) in choices:
                    if (nx + cx, ny + cy, nz + cz) in cube:
                        nx, ny, nz = nx + cx, ny + cy, nz + cz
                        ndx, ndy, ndz = cx, cy, cz
                        break
                else:
                    raise ValueError("Moved off the cube and couldn't find it again")
            if (nx, ny, nz) in cube and cube[(nx, ny, nz)] == "#":
                return (px, py, pz), (dx, dy, dz)
            px, py, pz = nx, ny, nz
            dx, dy, dz = ndx, ndy, ndz
        return (px, py, pz), (dx, dy, dz)


    (px, py, pz), (dx, dy, dz), (lx, ly, lz) = start
    for instruction in instructions:
        if instruction == "R" or instruction == "L":
            (dx, dy, dz), (lx, ly, lz) = rotation_map[((dx, dy, dz), (lx, ly, lz))][instruction]
        else:
            (px, py, pz), (dx, dy, dz) = run_step((px, py, pz), (dx, dy, dz), (lx, ly, lz), instruction)
    return (px, py, pz), (dx, dy, dz), (lx, ly, l)


def calculate_cube_size(grid):
    max_x = max(grid, key=lambda v:v[0])[0]
    max_y = max(grid, key=lambda v:v[1])[1]
    width = min(max_x, max_y)
    height = max(max_x, max_y)
    if width % 2 == 0 and height % 5 == 0 and height == width * 2.5:
        # single case where the net has a width of 2 * size
        return width // 2
    else:
        # all other nets have a width of 3 * size
        assert width % 3 == 0
        return width // 3


grid, instructions = parse_file("22_input.txt")
size = calculate_cube_size(grid)
segments = find_segments(grid, size)
transformations, origin = walk_segments(segments, size)

plane_to_cube, cube_to_plane = apply_mapping(grid, size, origin, transformations)
cube = {plane_to_cube[k]:grid[k] for k in grid}
assert len(plane_to_cube) == len(cube_to_plane)

start_pos = min((x, y) for (x, y) in grid if x == 1)
next_pos = start_pos[0], start_pos[1] + 1
start_pos_cube, next_pos_cube = plane_to_cube[(start_pos)], plane_to_cube[(next_pos)]
start_dir = tuple(v2 - v1 for (v1, v2) in zip(start_pos_cube, next_pos_cube))
start_left = (-1, 0, 0)

final_cube_pos, final_cube_dir, final_cube_left = run_instructions_cube(
        cube, instructions, (start_pos_cube, start_dir, start_left), cube_to_plane
)
final_plane = cube_to_plane[final_cube_pos]

# we need to reconstruct the direction we're facing on the plane
# at least one of the points ahead of behind us will be on the same face as us
forward_pos = tuple(p + d for p, d in zip(final_cube_pos, final_cube_dir))
reverse_pos = tuple(p - d for p, d in zip(final_cube_pos, final_cube_dir))
if forward_pos not in cube:
    assert reverse_pos in cube
    neighbour = reverse_pos
    sign = -1
else:
    neighbour = forward_pos
    sign = 1
plane_neighbour = cube_to_plane[neighbour]
delta = plane_neighbour[0] - final_plane[0], plane_neighbour[1] - final_plane[1]
delta = delta[0] * sign, delta[1] * sign
print(final_plane[0] * 1000 + final_plane[1] * 4 + facing_map[delta])
