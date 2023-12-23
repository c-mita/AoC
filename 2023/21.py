"""
For Part 1, we just do a BFS but with a trick of moving two steps at a time.
Fortunately, we're asked to move an "even" number of steps.


For Part 2...

First note there's a notion of polarity; a grid is either walked along an even
or odd number of steps and we need to track what it is.

The input also has a free row and column running along the centre. And a border
of empty cells. This means we can make a few assumptions.
Further, our input means we will walk an exact number of instaces of the grid.

Mark an "odd" grid as O and an even grid as "E".
We will end up with the following:

     E
    EOE
   EOEOE
  EOEOEOE
   EOEOE
    EOE
     E

But, the outer edge includes the inner corner of a few "odd" cells and
is missing the "outer" corner of the "even" cells.
The end caps are missing "two" corners.

Define "n" to be the nunber of "extra" cells walked in a cardinal direction
that is not our origin cell.
Then, the diagram above has:
 n = 3
 n*n odd cells (9)
 (n+1)*(n+1) odd cells (16)

 But we need to subtract the "missing" even corners.
 Because of symmetry, a missing corner is matched with the other three
 missing corners from the other edges of the diamond. That means we can just
 count the number of even cells on an edge, of which there are "n+1"

 We also need to add the odd corners that are missing above and the same
 symmetry applies. There are "n" per edge.


 T = (n+1)**2 * odd_cell + n**2 * even_cell - (n+1) * even_cell_corners + n * odd_cell_corners

 Note that this is a simple quadratic. We could calculate everything explicitly
 for a different values of the step size (moving in multiples of the length,
 i.e. increasing "n" by 1 each time) and use that to solve the quadratic as we
 did for Day 6.
"""


def parse_file(filename):
    space = {}
    start = None
    with open(filename) as f:
        for r, line in enumerate(f):
            for c, s in enumerate(line.strip()):
                if s == "S":
                    start = (r, c)
                if s != "#":
                    space[(r, c)] = "."
    return space, start


def step(pos, space):
    px, py = pos
    for np in ((px-1, py), (px+1, py), (px, py-1), (px, py+1)):
        if np in space:
            yield np


def two_steps(pos, space):
    visited = set()
    for s1 in step(pos, space):
        for s2 in step(s1, space):
            if s2 in visited:
                continue
            visited.add(s2)
            yield s2


def bfs(space, start, neighbour_func, steps=None):
    to_visit = list(start)
    visited = set(to_visit)
    while (steps is None or steps) and to_visit:
        next_visit = []
        for pos in to_visit:
            for np in neighbour_func(pos, space):
                if np in visited:
                    continue
                visited.add(np)
                next_visit.append(np)
        to_visit = next_visit
        if steps is not None:
            steps -= 1
    return len(visited)


space, start = parse_file("21.txt")

visited = bfs(space, [start], two_steps, steps=32)
print(visited)


total_steps = 26501365
max_r = max(k[0] for k in space)
min_r = min(k[0] for k in space)
max_c = max(k[1] for k in space)
min_c = min(k[1] for k in space)

assert max_r == max_c and min_c == min_r == 0
width = max_r + 1 - min_r
half_width = int(width // 2)
assert start[0] == half_width == start[1]
additional_blocks = (total_steps - half_width) / width

assert additional_blocks == int(additional_blocks)
additional_blocks = int(additional_blocks)
n = additional_blocks

cap_is_even = additional_blocks % 2 == 1

even_blocks = n*n
odd_blocks = (n+1) * (n+1)
if cap_is_even:
    odd_blocks, even_blocks = even_blocks, odd_blocks

positive_additions = n
negative_additions = n + 1
sx, sy = start
odd_start = [(sx-1, sy), (sx+1, sy), (sx, sy-1), (sx, sy+1)]
even_start = [start]
whole_even = bfs(space, even_start, two_steps)
whole_odd = bfs(space, odd_start, two_steps)
even_centre = bfs(space, even_start, two_steps, steps=half_width//2)
odd_centre = bfs(space, odd_start, two_steps, steps=half_width//2)

odd_corners = whole_odd - odd_centre
even_corners = whole_even - even_centre

to_add = odd_corners if cap_is_even else even_corners
to_subtract = even_corners if cap_is_even else odd_corners

total = odd_blocks * whole_odd + even_blocks * whole_even
total += positive_additions * to_add
total -= negative_additions * to_subtract
print(total)
