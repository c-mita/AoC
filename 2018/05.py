TEST_INPUT = "dabAcCaCBAcCcaDA"

CASE_BIT = 32

def process_polymer_string(polymer_string):
    polymer_stack = []
    for c in polymer_string:
        d = ord(c)
        if len(polymer_stack) == 0:
            polymer_stack.append(d)
        elif polymer_stack[-1] == d ^ CASE_BIT:
            polymer_stack.pop()
        else:
            polymer_stack.append(d)
    return "".join(chr(c) for c in polymer_stack)


def strip_polymer(polymer_string, to_remove):
    mask = ~CASE_BIT
    v = ord(to_remove) & mask
    return "".join(c for c in polymer_string if (ord(c) & mask) != v)


with open("05_input.txt") as f:
    polymer_string = f.readline().strip()

compressed_polymer = process_polymer_string(polymer_string)
print(len(compressed_polymer))

chars = [chr(x) for x in range(0x41, 0x41 + 26)]
stripped_polymers = [(c, strip_polymer(compressed_polymer, c)) for c in chars]
processed_polymers = [(c, process_polymer_string(s)) for (c, s) in stripped_polymers]

(worst_c, shortest_polymer) = min(processed_polymers, key=lambda cs: len(cs[1]))
print(len(shortest_polymer))
