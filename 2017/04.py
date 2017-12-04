def parse_file(filename):
    with open(filename) as f:
        return [l.strip() for l in f]

def is_valid(string):
    words = string.split()
    for (i, w) in enumerate(words):
        if w in words[i+1:]: return False
    return True

def is_valid_strong(string):
    words = string.split()
    for (i, w1) in enumerate(words):
        for w2 in words[i+1:]:
            if sorted(w1) == sorted(w2): return False
    return True

phrases = parse_file("04_input.txt")
print len([p for p in phrases if is_valid(p)])
print len([p for p in phrases if is_valid_strong(p)])
