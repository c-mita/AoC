import re

"""
Room = (name, id, checksum)
"""

def is_real(room):
    d = {}
    m = re.findall("[a-z]", room[0])
    for c in m:
        if c in d:
            d[c] += 1
        else:
            d[c] = 1
    def item_cmp(x, y):
        d = cmp(x[1], y[1])
        return d if d != 0 else cmp(y[0], x[0])
    check = [x[0] for x in sorted(d.items(), item_cmp, reverse=True)][:5]
    return "".join(check) == room[2]

def parse_room(line):
    name = re.split("[0-9]", line)[0][:-1] #stip last -
    id = int(re.findall("[0-9]+", line)[0])
    checksum = re.findall("[a-z]+", re.split("[0-9]+", line)[1])[0]
    return (name, id, checksum)

def parse_file(filename):
    with open(filename) as f:
        return [parse_room(line) for line in f]

def decrypt_room(room):
    name = room[0]
    shift = room[1]
    shift %= 26 # letters in alphabet
    decrypted = ""
    for c in name:
        if c == "-":
            decrypted += " "
            continue
        d = ord(c) - ord('a')
        d += shift
        d %= 26
        decrypted += chr(d + ord('a'))
    return decrypted


#print decrypt_room(("qzmt-zixmtkozy-ivhz", 343, []))

rooms = parse_file("4.txt")
real = [r for r in rooms if is_real(r)]
print sum([r[1] for r in real])

decrypted = [(decrypt_room(r), r[1]) for r in real]
print [d for d in decrypted if "north" in d[0]]
