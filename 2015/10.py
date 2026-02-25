"""
Honestly don't know a better way to solve this than just compute the sequence.
There may be some cleverness possible with the "elements" idea from Conway
(https://en.wikipedia.org/wiki/Look-and-say_sequence#Cosmological_decay) but
I cannot immediately see it.
"""

def look_say_increment(seq):
    def digit_runs(it):
        d = next(it)
        l = 1
        for c in it:
            if d == c:
                l += 1
            else:
                yield d, l
                d = c
                l = 1
        yield d, l

    new_seq = []
    for d, l in digit_runs(iter(seq)):
        new_seq.append(l)
        new_seq.append(d)
    return new_seq


def sequence_proc(seq, mapping):
    new_seq = []
    for d, l in consecutive_digits(iter(seq)):
        digits = tuple([d] * l)
        new_seq.extend(mapping[digits])
    return new_seq


INPUT = "1321131112"
initial_sequence = [ord(d) - ord("0") for d in INPUT]

seq = initial_sequence
for _ in range(40):
    seq = look_say_increment(seq)
print(len(seq))

for _ in range(10):
    seq = look_say_increment(seq)
print(len(seq))
