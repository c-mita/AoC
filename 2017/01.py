# Given sequence a(1), a(2), a(3), a(4),...
# Find sum of all a(i) where. a(i) == a(i+1)
# a(i_max) is followed by a(0) (so list loops)

def sum_of_matches(seq):
    seq_inc = seq[1:] + seq[0] # sequences starting "one ahead"
    sol_1 = sum((int(a) for (a, b) in zip(seq, seq_inc) if a == b))
    steps_ahead = len(seq) / 2
    seq_inc = seq[steps_ahead:] + seq[:steps_ahead]
    sol_2 = sum((int(a) for (a, b) in zip(seq, seq_inc) if a == b))
    return sol_1, sol_2

def parse_input(filename):
    with open(filename) as f:
        l = f.readline()
        return l.strip()

first_input = parse_input("01_input.txt")
print sum_of_matches(first_input)

