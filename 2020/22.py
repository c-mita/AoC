def parse_file(filename):
    with open(filename) as f:
        p1, p2 = f.read().strip().split("\n\n")
        return map(int, p1.split("\n")[1:]), map(int, p2.split("\n")[1:])


def play_game(p1, p2):
    p1, p2 = list(p1), list(p2)
    while p1 and p2:
        v1, v2 = p1.pop(0), p2.pop(0)
        if v1 > v2:
            p1.append(v1)
            p1.append(v2)
        else:
            p2.append(v2)
            p2.append(v1)
    return p1, p2


def memoise(func):
    # this doesn't help as much as I would have hoped :(
    cache = {}
    def wrapper(p1, p2):
        p1, p2 = tuple(p1), tuple(p2)
        if (p1, p2) in cache:
            v = cache[(p1, p2)]
            return v
        v = func(p1, p2)
        cache[(p1, p2)] = v
        return v
    return wrapper


@memoise
def play_recursive_game(p1, p2):
    seen = set()
    while p1 and p2:
        if (p1, p2) in seen or (p2, p1) in seen:
            return 1, p1, p2
        seen.add((p1, p2))
        v1, v2 = p1[0], p2[0]
        p1, p2 = p1[1:], p2[1:]
        if len(p1) < v1 or len(p2) < v2:
            if v1 > v2:
                p1 += (v1, v2)
            else:
                p2 += (v2, v1)
        else:
            w, r1, r2 = play_recursive_game(p1[:v1], p2[:v2])
            if w == 1:
                p1 += (v1, v2)
            else:
                p2 += (v2, v1)
    return len(p1) > len(p2), p1, p2


p1, p2 = parse_file("22.txt")
r1, r2 = play_game(p1, p2)
w = r1 if len(r1) else r2
print sum((n+1) * w for n, w in enumerate(reversed(w)))

p1, p2 = parse_file("22.txt")
w, r1, r2 = play_recursive_game(p1, p2)
w = r1 if w == 1 else r2
print sum((n+1) * w for n, w in enumerate(reversed(w)))
