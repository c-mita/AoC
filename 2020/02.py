from collections import namedtuple


record = namedtuple("record", ["lower", "upper", "letter", "password"])


def parsefile(filename):
    records = []
    with open(filename) as f:
        for l in f.readlines():
            password = l.split(": ")[1].strip()
            letter = l.split(":")[0][-1]
            limits = l.split(" ")[0].split("-")
            lower, upper = map(int, limits)
            records.append(record(lower, upper, letter, password))
    return records


def is_record_valid_1(r):
    v = r.password.count(r.letter)
    if r.lower <= v <= r.upper:
        return True
    return False


def is_record_valid_2(r):
    try:
        return (r.password[r.lower - 1] == r.letter) \
            != (r.password[r.upper - 1] == r.letter)
    except IndexError:
        return False


records = parsefile("02.txt")
print len([r for r in records if is_record_valid_1(r)])
print len([r for r in records if is_record_valid_2(r)])
