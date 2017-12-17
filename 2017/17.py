INPUT = 355
buffer = [0]
idx = 0
step = INPUT

for n in xrange(2017):
    idx = (idx + step) % len(buffer)
    idx += 1
    buffer.insert(idx, n + 1)
print buffer[idx + 1]

v = 0
idx = 0
for n in xrange(50*10**6):
    m = n + 1
    idx = (idx + step) % m
    if idx == 0: v = m
    idx += 1
print v
