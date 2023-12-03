import re

DIGITS = {
    "one":1,
    "two":2,
    "three":3,
    "four":4,
    "five":5,
    "six":6,
    "seven":7,
    "eight":8,
    "nine":9,
}
DIGITS.update({d:int(d) for d in "0123456789"})

def parse_input(filename):
    with open(filename) as f:
        return [l.strip() for l in f]

def calibration_value(line):
    def first_digit(s):
        for c in s:
            if c.isdigit():
                return int(c)
        raise ValueError("No digit")
    l = first_digit(line)
    r = first_digit(reversed(line))
    return l*10 + r


def advanced_calibration_value(line):
    # Need lookahead because our matches may overlap
    # nineight should return 98 - the "e" is used twice
    parts = re.findall("(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))", line)
    l = DIGITS[parts[0]]
    r = DIGITS[parts[-1]]
    return l*10 + r


data = parse_input("01.txt")

result = sum(calibration_value(l) for l in data)
print(result)

result = sum(advanced_calibration_value(l) for l in data)
print(result)
