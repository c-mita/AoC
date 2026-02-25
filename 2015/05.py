def parse_input(filename):
    with open(filename) as f:
        return [l.strip() for l in f]


def is_nice(line):
    def vowel_check():
        s = 0
        for c in line:
            if c in "aeiou":
                s += 1
                if s >= 3:
                    return True
        return False

    def doublet_check():
        for c1, c2 in zip(line[:-1], line[1:]):
            if c1 == c2:
                return True
        return False

    def bad_substrings_check():
        for bad in ["ab", "cd", "pq", "xy"]:
            if bad in line:
                return False
        return True

    return vowel_check() and doublet_check() and bad_substrings_check()


def is_nice_v2(line):
    def repeat_doublet_check():
        for idx in range(len(line) - 1):
            doublet = line[idx:idx+2]
            if doublet in line[idx+2:]:
                return True
        return False

    def straddle_check():
        for idx, c in enumerate(line[:-2]):
            if c == line[idx + 2]:
                return True
        return False

    return straddle_check() and repeat_doublet_check()


lines = parse_input("05.txt")
nice = [l for l in lines if is_nice(l)]
print(len(nice))

nice = [l for l in lines if is_nice_v2(l)]
print(len(nice))
