"""
Approach is to generate all invalid codes between the given bounds.

For part 2 we generate all base patterns for a given length and
then "repeat" it to fit within the bounds. Repeat for all possible
pattern lengths.
"""


def parse_ranges(range_string):
    for r in range_string.strip().split(","):
        left, right = r.split("-")
        yield left, right


def repeated_codes(bounds):
    lower_s, upper_s = bounds
    lower, upper = int(lower_s), int(upper_s)
    lower_half = lower_s[:len(lower_s) // 2]
    s = int(lower_half) if lower_half else 0
    m = 10**len(lower_half)

    while True:
        candidate = s * m + s
        if candidate > upper:
            break
        if candidate >= lower:
            yield candidate
        if s == m - 1:
            m *= 10
        s += 1


def numbers_of_length(length):
    start = 10 ** (length-1)
    yield from range(start, start * 10)


def candidates_for_length(pattern_length, lower, upper):
    m = 10 ** pattern_length
    for pattern in numbers_of_length(pattern_length):
        s = pattern * m + pattern
        while s < lower:
            s *= m
            s += pattern
        while s <= upper:
            yield s
            s *= m
            s += pattern


def repeated_n_codes(bounds):
    lower_s, upper_s = bounds
    lower, upper = int(lower_s), int(upper_s)
    max_length = len(upper_s) // 2
    for length in range(1, max_length + 1):
        yield from candidates_for_length(length, lower, upper)


TEST_STRING = (
    "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,"
    "1698522-1698528,446443-446449,38593856-38593862,565653-565659,"
    "824824821-824824827,2121212118-2121212124"
)

with open("02.txt") as f:
    data_string = f.readlines()[0].strip()

invalid_sum = 0
for r in parse_ranges(data_string):
    invalid_sum += sum(repeated_codes(r))
print(invalid_sum)

invalid_codes = set()
for r in parse_ranges(data_string):
    invalid_codes.update(repeated_n_codes(r))
print(sum(invalid_codes))
