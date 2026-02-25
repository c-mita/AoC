"""
Just implement the increment rules and test.
We can skip the symbols "i", "l" and "o" when calculating the increment
and we assume they don't appear in the input.

Part 2 is unsatisying; just do it again but this time it takes longer.
"""

def increment(password):
    symbols = "abcdefghjkmnpqrstuvwxyz"
    indexes = {c:symbols.index(c) for c in symbols}
    new_password = []
    to_add = 1
    for c in password:
        s_idx = indexes[c]
        idx = s_idx + to_add
        carry = int(idx // len(symbols))
        idx %= len(symbols)
        new_password.append(symbols[idx])
        to_add = carry
    if to_add:
        new_password.append(symbols[to_add-1])
    return new_password


def test_password(password):
    def test_triple():
        for a, b, c in zip(password[:-2], password[1:-1], password[2:]):
            if ord(a) == ord(b)+1 and ord(b) == ord(c)+1:
                return True
        return False

    def test_doublets():
        for idx in range(len(password)-1):
             a, b = password[idx], password[idx+1]
             if a == b:
                 break
        else:
            return False
        start = idx + 2
        for idx in range(start, len(password)-1):
             a, b = password[idx], password[idx+1]
             if a == b:
                 return True
        return False

    return test_triple() and test_doublets()


INPUT = "hxbxwxba"
TEST_INPUT = "abcdefgh"

start_password = [c for c in reversed(INPUT)]
password = start_password
while not test_password(password):
    password = increment(password)
print("".join(reversed(password)))

password = increment(password)
while not test_password(password):
    password = increment(password)
print("".join(reversed(password)))
