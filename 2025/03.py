"""
Quite straight forward; we can greedily select the first "maximal" element
in the sequence, accounting for the fact we must leave room for subsequent
choices.

That is, the next term will be the first "largest" value in the open
interval (idx, sequence_length - remaining_to_choose) where:

idx = index of the previously chosen element in the sequence
remaining_to_choose = how many elements we have to select.
"""


def parse_line(dataline):
    return list(map(int, (s for s in dataline)))


def largest_battery_pair(bank):
    first = 0
    second = 0
    idx = 0
    for n, v in enumerate(bank[:-1]):
        if v > first:
            first = v
            idx = n
    for n, v in enumerate(bank[idx+1:]):
        if v > second:
            second = v
    return first, second


def largest_battery_run(bank, length=12):
    if not length:
        return
    idx = 0
    max_v = 0
    for n, v in enumerate(bank):
        if n > len(bank) - length:
            break
        if v > max_v:
            max_v = v
            idx = n
    yield max_v
    # a good programmer would avoid copying the array on the recursion call
    yield from largest_battery_run(bank[idx+1:], length-1)


TEST_DATA = [
    "987654321111111",
    "811111111111119",
    "234234234234278",
    "818181911112111",
]

with open("03.txt") as f:
    data = [l.strip() for l in f]

banks = [parse_line(line) for line in data]
test_banks = [parse_line(line) for line in TEST_DATA]

s = 0
for bank in banks:
    first, second = largest_battery_pair(bank)
    s += first * 10 + second
print(s)

s = 0
for bank in banks:
    batteries = largest_battery_run(bank)
    v = 0
    for battery in batteries:
        v *= 10
        v += battery
    s += v
print(s)
