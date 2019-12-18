import intcode


test_string = """..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^.."""


class ROBOT_DIR:
    UP = 0, -1
    LEFT = -1, 0
    DOWN = 0, 1
    RIGHT = 0, 1

class ROBOT_TURN:
    LEFT = "L"
    RIGHT = "R"


def parse_input_file(filename):
    with open(filename) as f:
        return map(int, f.readlines()[0].split(","))

scaffold_points = set()
code = parse_input_file("17_input.txt")
vm = intcode.IntcodeVm(code)
grid_string = "".join(map(chr, vm.run()))

#grid_string = test_string

grid_line_strings = grid_string.split()
print grid_string

robot_pos = 0
robot_dir = 0
for y, line in enumerate(grid_line_strings):
    for x, c in enumerate(line):
        if c not in "." and c not in "X":
            scaffold_points.add((x, y))
        if c in "^v<>":
            robot_pos = (x, y)
            if c in "v": robot_dir = ROBOT_DIR.DOWN
            elif c in "^": robot_dir = ROBOT_DIR.UP
            elif c in ">": robot_dir = ROBOT_DIR.RIGHT
            elif c in "<": robot_dir = ROBOT_DIR.LEFT

# Part 1

intersection_points = []
# we assume an intersection point has at least three neighbours
for x, y in scaffold_points:
    n_count = 0
    if (x-1, y) in scaffold_points: n_count += 1
    if (x+1, y) in scaffold_points: n_count += 1
    if (x, y-1) in scaffold_points: n_count += 1
    if (x, y+1) in scaffold_points: n_count += 1
    if n_count > 2: intersection_points.append((x, y))

calibration_value = sum(x * y for (x, y) in intersection_points)
print calibration_value



# Part 2
# produce the path to move along scaffold
# try to compress into three blocks of steps that can be used as patterns
# recursively look for three blocks that cover the whole sequence
# format into sequences and pass into the IntCode VM


def get_run(scaffold_points, pos, direction):
    x, y = direction
    x1, y1 = (x + 1) % 2, (y + 1) % 2
    x2, y2 = -x1, -y1

    x, y = pos
    if (x+x1, y+y1) in scaffold_points:
        dx, dy = (x1, y1)
    elif (x+x2, y+y2) in scaffold_points:
        dx, dy = (x2, y2)
    else:
        raise ValueError("Halt")

    n = 1
    while (x + n*dx, y + n*dy) in scaffold_points:
        n += 1

    if direction[1]:
        robot_turn = ROBOT_TURN.LEFT if dx == direction[1] else ROBOT_TURN.RIGHT
    else:
        robot_turn = ROBOT_TURN.RIGHT if dy == direction[0] else ROBOT_TURN.LEFT
    return robot_turn, n - 1, (dx, dy), (x + (n-1) * dx, y + (n-1) * dy)


def calculate_full_path(scaffold_points, initial_pos, initial_dir):
    path = []
    pos = initial_pos
    direction = initial_dir
    try:
        while True:
            turn, steps, direction, pos = get_run(scaffold_points, pos, direction)
            path.append((turn, steps))
    except ValueError:
        return path


def stringify_path(path):
    output = ""
    for d, n in path:
        output += "R" if d == ROBOT_TURN.RIGHT else "L"
        output += ","
        output += str(n)
        output += ","
    return output


def find_subsequences(sequences, depth):
    if depth > 2 and sequences:
        raise StopIteration("Failed")
    if not sequences:
        return []

    found_sequences = []

    seq = sequences[0]
    count = 0
    idx = 0
    n = 0

    while count <= 20:
        n += 1
        while n < len(seq) and seq[n] != ',':
            n+=1
        count += 1
        subsq = seq[:n+1]

        next_sequences = sum((seq.split(subsq) for seq in sequences), [])
        next_sequences = [s for s in next_sequences if s != '']

        try:
            return [subsq] + find_subsequences(next_sequences, depth + 1)
        except StopIteration:
            continue

    raise StopIteration("Failed to find pattern!")


def make_sequence_pattern(path, sequences):
    if not path:
        return []
    if not sequences:
        assert not path
        return []
    seq = sequences[0]
    output = []
    components = path.split(seq)
    for c in components[:-1]:
        output.extend(make_sequence_pattern(c, sequences[1:]))
        output.append(seq)
    output.extend(make_sequence_pattern(components[-1], sequences[1:]))
    return output


full_path = calculate_full_path(scaffold_points, robot_pos, robot_dir)
full_path_string = stringify_path(full_path)
sequences = find_subsequences([full_path_string], 0)

pattern = make_sequence_pattern(full_path_string, sequences)
pattern_map = {}
key = 0
for p in pattern:
    if p not in pattern_map:
        pattern_map[p] = key
        key += 1
reduced_pattern = [pattern_map[p] for p in pattern]
pattern_list = [x[0] for x in sorted(pattern_map.items(), key=lambda x:x[1])]

pattern_ascii = ','.join(chr(p + 0x41) for p in reduced_pattern)
assert len(pattern_ascii) < 20
for p in pattern_list:
    assert len(p) < 20


# verify patterns expand out properly
rev_map = {v:k for (k, v) in pattern_map.items()}
expanded_pattern = [rev_map[k] for k in reduced_pattern]
back_calced_string = "".join(expanded_pattern)
assert back_calced_string == full_path_string


def input_generator(pattern_ascii, pattern_list):
    for p in pattern_ascii:
        yield ord(p)
    yield ord('\n')

    for pattern in pattern_list:
        # trim away the final ','
        for v in pattern[:-1]:
            yield ord(v)
        yield ord('\n')

    yield ord('n')
    yield ord('\n')


code = parse_input_file("17_input.txt")
code[0] = 2
vm = intcode.IntcodeVm(code, input_generator(pattern_ascii, pattern_list))
output = vm.run()

grid_string = "".join(map(chr, output[:-1]))
grid_line_strings = grid_string.split()

print output[-1]
