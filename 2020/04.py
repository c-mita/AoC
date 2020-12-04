def parse_from_file(filename):
    with open(filename) as f:
        record = {}
        for line in f:
            if line == "\n":
                yield record
                record = {}
                continue
            fields = line.split(" ")
            for f in fields:
                k,v = f.split(":")
                record[k] = v.strip()
        yield record


def is_valid(record):
    for k in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]:
        if k not in record:
            return False
    return True


def is_valid_2(record):
    try:
        if not is_valid(record):
            return False
        if not (1920 <= int(record["byr"]) <= 2002):
            return False
        if not (2010 <= int(record["iyr"]) <= 2020):
            return False
        if not (2020 <= int(record["eyr"]) <= 2030):
            return False

        height = int(record["hgt"][:-2])
        if "cm" == record["hgt"][-2:]:
            if not (150 <= height <= 193):
                return False
        elif "in" == record["hgt"][-2:]:
            if not (59 <= height <= 76):
                return False
        else:
            return False

        if len(record["hcl"]) != 7 or record["hcl"][0] != "#":
            return False
        for c in record["hcl"][1:]:
            if c not in "0123456789abcdef":
                return False

        if record["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            return False

        if len(record["pid"]) != 9:
            return False
        for c in record["pid"]:
            if c not in "0123456789":
                return False
    except (IndexError, ValueError) as e:
        return False
    return True


records = list(parse_from_file("04.txt"))
print sum(1 for v in records if is_valid(v))
print sum(1 for v in records if is_valid_2(v))
