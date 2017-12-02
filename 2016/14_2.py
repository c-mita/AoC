import hashlib
import re
import time

"""
Variation of previous solution - look for a hash with 5 repeated digits
then check if a 3 matching it exists.
Runs in half the time of the previous.
"""

def make_md5(key, idx):
    return hashlib.md5("%s%s" % (key, idx)).hexdigest()

def make_stretched_md5s(key, idx):
    s = "%s%s" % (key, idx)
    for i in xrange(2017):
        s = hashlib.md5(s).hexdigest()
    return s

def get_keys(key, hashfunc):
    keys = []
    idx = 0
    five_match = re.compile(r"(.)\1{4,}")
    three_match = re.compile(r"(.)\1{2,}")
    hash3 = {}
    # hashes are generated slightly out of order - len test not enough
    while len(keys) <= 64 or (idx - keys[-1][0] <= 1000):
        md5 = hashfunc(key, idx)
        match = five_match.search(md5)
        if match:
            char = match.group()[0]
            for (jdx, h) in hash3.get(char, []):
                if idx - jdx <= 1000:
                    keys.append((jdx, h))
            # needs to be sorted for range check to work in loop test
            hash3[char] = [] # can't reuse a "3 match" - must only be counted
            keys.sort()
        match = three_match.search(md5)
        if match:
            hash3.setdefault(match.group()[0], []).append((idx, md5))
        idx += 1
    return keys

start_time = time.time()
result = get_keys("cuanljph", make_stretched_md5s)
print result[63]
print time.time() - start_time
