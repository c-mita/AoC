import re

def parse_marker(marker):
    values = re.findall("[0-9]+", marker)
    return int(values[0]), int(values[1])

def decompress_rec(s_in):
    s_out = ""
    marker = r"\([0-9]+x[0-9]+\)"
    rp = re.compile(marker)
    match = rp.search(s_in)
    while match:
        s_out += s_in[0:match.start()]
        length, repeat = parse_marker(match.group())
        s_in = s_in[match.end():]
        s_segment = s_in[0:length] * repeat
        s_in = s_segment + s_in[length:]
        match = rp.search(s_in)
        print len(s_out)
    s_out += s_in
    return s_out

# I think this is wrong,
# should fail on (5x2)(5x2)ABCDEF
def calc_dec_length_rec(s_in, scale=1):
    marker = r"\([0-9]+x[0-9]+\)"
    rp = re.compile(marker)
    match = rp.search(s_in)
    pos = 0
    total_length = 0
    while match:
        total_length += match.start() - pos
        length, repeat = parse_marker(match.group())
        pos = match.end()
        segment = s_in[pos:pos+length]
        pos += length
        total_length += calc_dec_length_rec(segment, repeat)
        match = rp.search(s_in, pos)
    total_length += len(s_in[pos:])
    total_length *= scale
    return total_length

def decompress(s_in):
    s_out = ""
    marker = r"\([0-9]+x[0-9]+\)"
    rp = re.compile(marker)
    pos = 0
    match = rp.search(s_in, pos)
    while match:
        s_out += s_in[pos:match.start()]
        length, repeat = parse_marker(match.group())
        pos = match.end()
        s_segment = s_in[pos:pos+length] * repeat
        s_out += s_segment
        pos += length
        match = rp.search(s_in, pos)
    s_out += s_in[pos:]
    return s_out

def parse_file(filename):
    with open(filename) as f:
        return "".join([line for line in f]).strip()

def decompress_file(filename, recursive):
    with open(filename) as f:
        if recursive:
            lines = [decompress_rec(line) for line in f]
        else:
            lines = [decompress(line) for line in f]
    return "".join(lines).strip()

out = decompress_file("9.txt", False)
print len(out)

#print calc_dec_length_rec("(3x3)XYZ")
#print calc_dec_length_rec("(27x12)(20x12)(13x14)(7x10)(1x12)A")
#print calc_dec_length_rec("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN")
#print calc_dec_length_rec("(3x1)TWO(5x1)SEVEN")
#print calc_dec_length_rec("(3x2)TWO(5x7)SEVEN")

#print calc_dec_length_rec("(5x2)(5x2)ABCDEFHIJK")

print calc_dec_length_rec(parse_file("9.txt"))
