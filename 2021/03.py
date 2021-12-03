def parse_input(filename):
    bit_arrays = []
    with open(filename) as f:
        return [map(int, (c for c in l.strip())) for l in f]

def bits_to_int(bit_array):
    v = 0
    for b in bit_array:
        v = v * 2 + b
    return v

def most_common_bit(arrays, digit):
    s = sum(a[digit] for a in arrays)
    # if there are more 1s than 0s, then the sum must exceed half the length of the array
    # bias towards 1 to match problem description (including when inverted for CO2 case)
    return 1 if s >= 0.5 * len(arrays) else 0

bit_arrays = parse_input("03_input.txt")
bit_length = len(bit_arrays[0])
sums = [0] * bit_length
for bits in bit_arrays:
    for n, v in enumerate(bits):
        sums[n] += v
# if 1 is more common than 0, then sums[n] > 0.5 * len(arrays) for each n
most_common_bits = [1 if v > 0.5 * len(bit_arrays) else 0 for v in sums]
least_common_bits = [0 if v else 1 for v in most_common_bits]

gamma = bits_to_int(most_common_bits)
epsilon = bits_to_int(least_common_bits)
print(gamma * epsilon)

oxygen_numbers = bit_arrays
scrubber_numbers = bit_arrays
for n in range(bit_length):
    if len(oxygen_numbers) > 1:
        v = most_common_bit(oxygen_numbers, n)
        oxygen_numbers = [array for array in oxygen_numbers if array[n] == v]
    if len(scrubber_numbers) > 1:
        v = most_common_bit(scrubber_numbers, n)
        v = 0 if v else 1
        scrubber_numbers = [array for array in scrubber_numbers if array[n] == v]

oxygen = bits_to_int(oxygen_numbers[0])
scrubber = bits_to_int(scrubber_numbers[0])
print(oxygen * scrubber)
