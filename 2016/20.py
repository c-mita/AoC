import operator
from time import time

def parse_file(filename):
    with open(filename) as f:
        return [(int(x), int(y)) for x, y in [line.split("-") for line in f]]

def find_lowest_valid(excluded):
    """lowest will be r_stop + 1 for one of the excluded pairs or zero"""
    excluded = list(excluded)
    excluded.append((-1, -1)) #so we can get 0 as an answer if not excluded
    excluded.sort(key=operator.itemgetter(1))
    for r_start, r_stop in excluded:
        for r2_start, r2_stop in excluded:
            #print r2_start, r_stop + 1, r2_stop
            if r2_start <= r_stop + 1 <= r2_stop: break
        else: return r_stop + 1
    return None

def combine_overlapped(excluded):
    """combine overlapping regions"""
    excluded = list(excluded)
    for i in xrange(len(excluded)):
        for j in xrange(i + 1, len(excluded)):
            if excluded[i] == None or excluded[j] == None: continue
            r1_start, r1_stop = excluded[i]
            r2_start, r2_stop = excluded[j]
            if r1_start <= r2_start and r2_stop <= r1_stop:
                excluded[j] = None
            elif r1_start <= r2_start <= r1_stop <= r2_stop:
                excluded[i] = (r1_start, r2_stop)
                excluded[j] = None
            elif r2_start <= r1_start and r1_stop <= r2_stop:
                excluded[i] = None
            elif r2_start <= r1_start <= r2_stop <= r1_stop:
                excluded[j] = (r2_start, r1_stop)
                excluded[i] = None
    return [e for e in excluded if e is not None]

def find_number_of_valid(excluded, maximum):
    while True:
        combined = combine_overlapped(excluded)
        if len(excluded) == len(combined): break
        excluded = combined
    n = maximum + 1
    for r_start, r_stop in excluded:
        n -= r_stop - r_start + 1
    return n

#pairs = parse_file("20_test.txt")
pairs = parse_file("20.txt")
test = [(5, 8), (0, 2), (4, 7)]
st = time()
print find_lowest_valid(pairs)
print time() - st
st = time()
print find_number_of_valid(pairs, 0xFFFFFFFF)
print time() - st
