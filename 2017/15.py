INPUT_A, INPUT_B = 512, 191
factor_a, factor_b = 16807, 48271

ga, gb = INPUT_A, INPUT_B
matches = 0
for n in xrange(40*10**6):
    ga = (factor_a * ga) % 0x7FFFFFFF
    gb = (factor_b * gb) % 0x7FFFFFFF
    if gb & 0xFFFF == ga & 0xFFFF: matches += 1
print matches

ga, gb = INPUT_A, INPUT_B
matches = 0
n = 0
while n < 5 * 10**6:
    ga = (factor_a * ga) % 0x7FFFFFFF
    gb = (factor_b * gb) % 0x7FFFFFFF
    while ga & 0x3 != 0:
        ga = (factor_a * ga) % 0x7FFFFFFF
    while gb & 0x7 != 0:
        gb = (factor_b * gb) % 0x7FFFFFFF
    if gb & 0xFFFF == ga & 0xFFFF: matches += 1
    n += 1

print matches
