import hashlib


def md5_hex(key):
    return hashlib.md5(key).hexdigest()


def key_gen(key):
    n = 1
    while True:
        yield (str.encode("%s%s" % (key, n), encoding="ascii"), n)
        n += 1


def run_to_condition(key_root, condition):
    for key, n in key_gen(key_root):
        h = md5_hex(key)
        if condition(h):
            return n


five_zeros = lambda s: s.startswith("00000")
n  = run_to_condition("yzbqklnj", five_zeros)
print(n)

six_zeros = lambda s: s.startswith("000000")
n  = run_to_condition("yzbqklnj", six_zeros)
print(n)
