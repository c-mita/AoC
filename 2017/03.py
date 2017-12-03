import math

"""
Part 1:
Grid pattern is:
17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...

Say 1 is at position (0, 0).
Value N is contained within the smallest n*n ring where n is odd and n > sqrt(N)
This ring starts at position ((n-1)/2, (1-n)/2 + 1) with value (n-2)*(n-2) + 1

The corners of the ring are: ((n-1)/2, (n-1)/2), ((1-n)/2, (n-1)/2), ((1-n)/2, (1-n)/2), ((n-1)/2, (1-n)/2)
Do repeated subtractions to find the segment and distance along final segmant.


Part 2:
Just fill the virtual grid until you write a value larger than the test value
"""

def calc_coords(value):
    n = int(math.ceil(math.sqrt(value)))
    if n & 1 == 0: n += 1
    v_start = (n-2)**2 + 1
    diff = value - v_start
    if diff < n - 2:
        return ((n-1) / 2, (1-n) / 2 + 1 + diff)
    diff -= n - 2
    if diff < n - 1:
        return ((n-1) / 2 - diff, (n-1) / 2)
    diff -= n - 1
    if diff < n - 1:
        return ((1-n) / 2, (n-1) / 2 - diff)
    diff -= n - 1
    return ((1-n) / 2 + diff, (1-n) / 2)

def fill_grid_with_sums(target_sum):
    grid = {(0, 0):1}
    idx = 2
    s = 1
    while s < target_sum:
        px, py = calc_coords(idx)
        s = grid.setdefault((px-1, py-1), 0) \
                + grid.setdefault((px, py-1), 0) \
                + grid.setdefault((px+1, py-1), 0) \
                + grid.setdefault((px-1, py), 0) \
                + grid.setdefault((px+1, py), 0) \
                + grid.setdefault((px-1, py+1), 0) \
                + grid.setdefault((px, py+1), 0) \
                + grid.setdefault((px+1, py+1), 0)
        grid[(px, py)] = s
        idx += 1
    return s, grid

print sum(abs(n) for n in calc_coords(325489))
s, grid = fill_grid_with_sums(325489)
print s
