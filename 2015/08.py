def parse_input(filename):
    with open(filename) as f:
        return [l.strip() for l in f]


def to_bytes(s):
    def decode_hex(src):
        x1 = next(src)
        x2 = next(src)
        v = int(x1 + x2, 16)
        yield v

    def decode_escape(src):
        c = next(src)
        if c == "\\" or c == "\"":
            yield ord(c)
        elif c == "x":
            yield from decode_hex(src)
        else:
            raise ValueError("Bad escape sequence \\%s" % c)

    def decode_string(src):
        c = next(src)
        if c != "\"":
            raise ValueError("Must start with '\"'")
        for c in src:
            if c == "\\":
                yield from decode_escape(src)
            elif c == "\"":
                break
            else:
                yield ord(c)
        if not c == "\"":
            raise ValueError("Non terminated string")

    return [b for b in decode_string(iter(s))]


def encode(s):
    def encode_char(c):
        if c == "\"":
            return "\\\""
        elif c == "\\":
            return "\\\\"
        else:
            return c
    chars = (encode_char(c) for c in s)
    return "\"" + "".join(chars) + "\""


data = parse_input("08.txt")

mem_diff = 0
for l in data:
    mem_diff += len(l) - len(to_bytes(l))
print(mem_diff)

mem_diff = 0
for l in data:
    mem_diff += len(encode(l)) - len(l)
print(mem_diff)
