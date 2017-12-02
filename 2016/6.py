import operator

def process_lines(lines, inverse):
    answer = ""
    for i in xrange(len(lines[0])):
        d = {}
        for line in lines:
            c = line[i]
            d[c] = d[c] + 1 if c in d else 1
        v = [c[0] for c in sorted(
            d.items(), key=operator.itemgetter(1), reverse=not inverse)][0]
        answer += v
    return answer



def parse_file(filename):
    with open(filename) as f:
        return [line for line in f]

TEST = """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar"""

print process_lines(parse_file("6.txt"), False)
print process_lines(parse_file("6.txt"), True)
