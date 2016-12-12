RECT = 1
SHIFT_R = 2
SHIFT_C = 3

screen = [[0] * 50 for i in range(6)]

def screen_string(arr):
    s = ""
    for row in screen:
        for d in row:
            s += "# " if d else ". "
        s += "\n"
    return s

def count_on(arr):
    s = 0
    for row in screen:
        s += sum(row)
    return s

def process_command(command, args, arr):
    if command == RECT:
        a, b = args[0], args[1]
        for i in xrange(b):
            for j in xrange(a):
                arr[i][j] = 1
    elif command == SHIFT_R:
        row = args[0]
        shift = args[1]
        old_r = arr[row]
        new_r = [old_r[(i - shift) % len(old_r)] for i in xrange(len(old_r))]
        arr[row] = new_r
    elif command == SHIFT_C:
        column = args[0]
        shift = args[1]
        old_c = [row[column] for row in arr]
        new_c = [old_c[(i - shift) % len(old_c)] for i in xrange(len(old_c))]
        for row, c in zip(arr, new_c):
            row[column] = c

def parse_line(line):
    if line.startswith("rect"):
        args = tuple(int(x) for x in line.strip("rect ").split("x"))
        return (RECT, args)
    elif line.startswith("rotate row y="):
        args = tuple(int(x) for x in line.strip("rotate row y=").split(" by "))
        return (SHIFT_R, args)
    elif line.startswith("rotate column x="):
        args = tuple(int(x) for x in line.strip("rotate column x=").split(" by "))
        return (SHIFT_C, args)
    else:
        raise ValueError("UNKNOWN COMMAND")

def parse_file(filename):
    with open(filename) as f:
        return [parse_line(line) for line in f]

commands = parse_file("8.txt")
for command in commands:
    process_command(command[0], command[1], screen)
print screen_string(screen)
print count_on(screen)

# If I was really clever and not terribly lazy, I would try to pattern match
# the screen contents to produce the resulting code. But I *am* terribly lazy,
# to say nothing of my intelligence.
