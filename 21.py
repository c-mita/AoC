import re

SWAP_POSITION = 1
SWAP_LETTER = 2
ROTATE_LEFT = 3
ROTATE_RIGHT = 4
ROTATE_LETTER = 5
REVERSE_XY = 6
MOV_POS = 7

def parse_instruction(line):
    positions = map(int, re.findall("[0-9]+", line))
    letters = [s[-1] for s in re.findall("letter [a-z]", line)]
    if line.startswith("swap position"):
        return (SWAP_POSITION, positions[0], positions[1])
    elif line.startswith("swap letter"):
        return (SWAP_LETTER, letters[0], letters[1])
    elif line.startswith("rotate left"):
        return (ROTATE_LEFT, positions[0], None)
    elif line.startswith("rotate right"):
        return (ROTATE_RIGHT, positions[0], None)
    elif line.startswith("rotate based"):
        return (ROTATE_LETTER, letters[0], None)
    elif line.startswith("reverse positions"):
        return (REVERSE_XY, positions[0], positions[1])
    elif line.startswith("move"):
        return (MOV_POS, positions[0], positions[1])
    raise ValueError("UNKNOWN INSTRUCTION: %s" % line)

def parse_file(filename):
    with open(filename) as f:
        return [parse_instruction(line) for line in f]

def swap_position(s, p1, p2):
    s = list(s)
    s[p1], s[p2] = s[p2], s[p1]
    return "".join(s)

def swap_letter(s, l1, l2):
    s = list(s)
    for i in xrange(len(s)):
        if s[i] == l1: s[i] = l2
        elif s[i] == l2: s[i] = l1
    return "".join(s)

def rotate_left(s, n):
    n %= len(s)
    return s[n:] + s[:n]

def rotate_letter(s, l):
    if l not in s: return s
    n = s.index(l)
    n = 1 + n if n < 4 else 2 + n
    return rotate_left(s, 0-n)

def reverse_region(s, start, end):
    return s[:start] + s[end:None if start==0 else start-1:-1] + s[end+1:]

def move_x_y(s, p1, p2):
    s = list(s)
    s.insert(p2, s.pop(p1))
    return "".join(s)

def reverse_rotate_letter(s, l):
    # just rotate left until it works
    p = rotate_left(s, 1)
    while rotate_letter(p, l) != s:
        p = rotate_left(p, 1)
    return p

def apply_mutation(s, mutation):
    command, arg1, arg2 = mutation
    if command == SWAP_POSITION:
        return swap_position(s, arg1, arg2)
    elif command == SWAP_LETTER:
        return swap_letter(s, arg1, arg2)
    elif command == ROTATE_LEFT:
        return rotate_left(s, arg1)
    elif command == ROTATE_RIGHT:
        return rotate_left(s, 0-arg1)
    elif command == ROTATE_LETTER:
        return rotate_letter(s, arg1)
    elif command == REVERSE_XY:
        return reverse_region(s, arg1, arg2)
    elif command == MOV_POS:
        return move_x_y(s, arg1, arg2)
    else:
        raise ValueError("UNKNOWN COMMAND %s" % str(mutation))

def apply_inverse_mutation(s, mutation):
    command, arg1, arg2 = mutation
    if command == SWAP_POSITION:
        return swap_position(s, arg2, arg1)
    elif command == SWAP_LETTER:
        return swap_letter(s, arg2, arg1)
    elif command == ROTATE_LEFT:
        return rotate_left(s, 0-arg1)
    elif command == ROTATE_RIGHT:
        return rotate_left(s, arg1)
    elif command == ROTATE_LETTER:
        return reverse_rotate_letter(s, arg1)
    elif command == REVERSE_XY:
        return reverse_region(s, arg1, arg2)
    elif command == MOV_POS:
        return move_x_y(s, arg2, arg1)
    else:
        raise ValueError("UNKNOWN COMMAND %s" % str(mutation))


instructions = parse_file("21.txt")
test_instructions = [
    (SWAP_POSITION, 4, 0),
    (SWAP_LETTER, "d", "b"),
    (REVERSE_XY, 0, 4),
    (ROTATE_LEFT, 1, None),
    (MOV_POS, 1, 4),
    (MOV_POS, 3, 0),
    (ROTATE_LETTER, "b", None),
    (ROTATE_LETTER, "d", None)
]
p = "abcdefgh"
for ins in instructions:
    p = apply_mutation(p, ins)
print p

p = "fbgdceah"
for ins in instructions[::-1]:
    p = apply_inverse_mutation(p, ins)
print p
