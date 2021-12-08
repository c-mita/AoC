"""
For part 2, we just brute force the problem.
We could probably try something clever, but 7! just isn't a very big number.
(Obviously, this takes whole seconds to run).
"""

import itertools

SYMBOLS = {
    "abcefg" : 0,
    "cf" : 1,
    "acdeg" : 2,
    "acdfg" : 3,
    "bcdf" : 4,
    "abdfg" : 5,
    "abdefg" : 6,
    "acf" : 7,
    "abcdefg" : 8,
    "abcdfg" : 9,
}

def parse_file(filename):
    signals = []
    with open(filename) as f:
        for line in f:
            inputs, outputs = map(lambda v: v.split(), line.strip().split(" | "))
            signals.append((inputs, outputs))
    return signals


def valid_mapping(signal, mapping):
    mapped_signal = "".join(sorted(mapping[c] for c in signal))
    return mapped_signal in SYMBOLS


def solve_signal_set(signals):
    symbols = "abcdefg"
    for target_set in itertools.permutations(symbols):
        target_set = "".join(target_set)
        mapping = {s:t for (s,t) in zip(symbols, target_set)}
        if all(valid_mapping(signal, mapping) for signal in signals):
            return mapping
    raise ValueError("No valid mappings")


signals = parse_file("08_input.txt")
count_1478 = 0
for input_signal, output_signal in signals:
    for signal in output_signal:
        l = len(signal)
        count_1478 += int(l == 2 or l == 4 or l == 3 or l == 7)
print(count_1478)

s = 0
for in_signal, out_signal in signals:
    union = in_signal + out_signal
    mapping = solve_signal_set(union)
    out_number = 0
    for signal in out_signal:
        segments = "".join(sorted(mapping[c] for c in signal))
        out_number = out_number * 10 + SYMBOLS[segments]
    s += out_number
print(s)
