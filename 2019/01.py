def parse_input(filename):
    with open(filename) as f:
        return map(int, f.readlines())

masses = parse_input("01_input.txt")

# Part 1 - just apply formula
fuel_func = lambda m: m / 3 - 2
total = sum((fuel_func(m) for m in masses))
print total

# Part 2 - more complicated module function
def fuel_calc(mass):
    fuel = 0
    f = mass
    while f > 0:
        f = f / 3 - 2
        if f > 0:
            fuel += f
    return fuel

total = sum((fuel_calc(m) for m in masses))
print total
