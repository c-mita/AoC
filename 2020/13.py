def parse_file(filename):
    with open(filename) as f:
        time, ids = (l.strip() for l in f)
        time = int(time)
        return time, [(n, int(i)) for (n, i) in enumerate(ids.split(",")) if i != "x"]


def mod_inv(a, m):
    t, t2 = 0, 1
    r, r2 = m, a
    while r2:
        q = r / r2
        t, t2 = t2, t - q*t2
        r, r2 = r2, r - q*r2
    if r > 1: raise ValueError("No inverse")
    if t < 0: t += m
    return t


start_t, ids = parse_file("13.txt")
#start_t = 939
#ids = [(0, 7), (1, 13), (4, 59), (6, 31), (7, 19)]

min_d, min_id = max(ids), -1
for t, n in ids:
    d = n - start_t % n
    (min_d, min_id) = (d, n) if d < min_d else (min_d, min_id)
print min_id * min_d


"""
Our ids are (relative_offset, time_gap)
We note all time_gaps are prime, so chinese remainder theorem applies
[(k1, x1), (k2, x2), .... (kn, xn)]
ai == ki mod xi
"""
# we invert the id because we're seeking the time "before" it arrives...
x = [xi for (ki, xi) in ids]
k = [-ki for (ki, xi) in ids]
X = reduce(lambda v1,v2: v1*v2, x)
y = [X/xi for xi in x]
z = [mod_inv(yi, xi) for (yi, xi) in zip(y, x)]

a = sum(ki * yi * zi for (ki, yi, zi) in zip(k, y, z))
print a % X
