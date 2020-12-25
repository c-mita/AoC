INPUT_1 = 6929599
INPUT_2 = 2448427
MOD = 20201227


def find_loop_size(target, subject=7, mod=MOD):
    v = 1
    n = 0
    while v != target:
        v = (v * subject) % mod
        n += 1
    return n


loop = find_loop_size(INPUT_2)
print pow(INPUT_1, loop, MOD)
