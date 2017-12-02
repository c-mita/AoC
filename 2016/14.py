import hashlib
import re
import time

def make_md5s(start_idx, stop_idx, key):
    return [hashlib.md5("%s%s" % (key, i)).hexdigest()
        for i in xrange(start_idx, stop_idx)]

def make_stretched_md5s(start_idx, stop_idx, key):
    def nhash(s, n):
        for i in xrange(n):
            s = hashlib.md5(s).hexdigest()
        return s
    return [nhash("%s%s" % (key, i), 2017)
            for i in xrange(start_idx, stop_idx)]

def get_keys(key, n, hashfunc):
    md5s = []
    idx = 0
    jdx = 0
    keys = []
    trip_match = re.compile(r"(.)\1\1")
    while len(keys) < n:
        for m5 in md5s:
            jdx += 1
            match = trip_match.search(m5)
            if match:
                char = match.groups()[0]
                five_match = re.compile(char * 5)
                md5s = md5s[jdx:] + hashfunc(len(md5s) + idx - jdx + 1, idx + 1001, key)
                jdx = 0
                for m5_2 in md5s:
                    if five_match.search(m5_2):
                        keys.append((idx, m5))
                        print idx, m5
                        break
            idx += 1
        md5s = hashfunc(idx, idx+1000, key)
        jdx = 0
    return keys

test_key = "abc"
key = "cuanljph"

start_time = time.time()
print get_keys(test_key, 64, make_md5s)[63]
print time.time() - start_time
start_time = time.time()
print get_keys(key, 64, make_stretched_md5s)[63]
print time.time() - start_time
