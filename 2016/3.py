def is_valid_triangle(lengths):
    lengths.sort()
    return lengths[0] + lengths[1] > lengths[2]

def parse_line(line):
    return [int(s) for s in line.split(None)]

def parse_file(file_name):
    lines = []
    with open(file_name) as f:
        for line in f:
            lines.append(parse_line(line))
    return lines

def parse_file_2(file_name):
    t1, t2, t3 = [], [], []
    triangles = []
    with open(file_name) as f:
        i = 1
        for line in f:
            v1, v2, v3 = parse_line(line)[:3]
            t1.append(v1)
            t2.append(v2)
            t3.append(v3)
            if i % 3 == 0:
                triangles += [t1, t2, t3]
                t1, t2, t3 = [], [], []
            i += 1
    return triangles

lines = parse_file("3.txt")
valid = [line for line in lines if is_valid_triangle(line)]
print len(valid)

lines = parse_file_2("3.txt")
valid = [line for line in lines if is_valid_triangle(line)]
print len(valid)
