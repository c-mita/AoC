def parse_input(filename):
    with open(filename) as f:
         return [int(n) for n in [l.split() for l in f.readlines()][0]]

def run_cycle(banks):
    idx = banks.index(max(banks))
    blocks = banks[idx]
    banks[idx] = 0
    n = len(banks)
    while blocks > 0:
        idx += 1
        idx %= n
        banks[idx] += 1
        blocks -= 1
    return banks

def iterate_cycles(starting_banks):
    loops = 0
    banks = list(starting_banks)
    prev_arrangements = {}
    bank_tuple = tuple(banks)
    while bank_tuple not in prev_arrangements:
        prev_arrangements[bank_tuple] = loops
        banks = run_cycle(banks)
        bank_tuple = tuple(banks)
        loops += 1
    return loops, loops - prev_arrangements[bank_tuple], banks

#print iterate_cycles([0, 2, 7, 0])
starting_config = parse_input("06_input.txt")
print iterate_cycles(starting_config)
