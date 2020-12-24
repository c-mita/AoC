def cycle(data, v):
    """
    Data is an array mapping index->next_index
    that is, a[i] is the successor to i
    """
    min_v, max_v = 1, len(data) - 1
    v1 = data[v]
    v2 = data[v1]
    v3 = data[v2]
    data[v] = data[v3]
    d = v - 1
    if d < min_v: d = max_v
    while d in [v1, v2, v3]:
        d -= 1
        if d < min_v: d = max_v
    data[v3] = data[d]
    data[d] = v1
    return data[v]


def array_string(data, i=1):
    s = ""
    for n in range(len(data) - 1):
        s += str(i)
        i = data[i]
    return s


def create_array(digits):
    digits = map(int, (c for c in digits))
    data = [0] * (len(digits) + 1)
    for d, s in zip(digits[:-1], digits[1:]):
        data[d] = s
    data[digits[-1]] = digits[0]
    return data



TEST_INPUT = "389125467"
INPUT = "394618527"

data = create_array(INPUT)
initial_v = 3
v = initial_v
for n in range(100):
    v = cycle(data, v)
print array_string(data, 1)[1:]

digits = [n+1 for n in xrange(10**6)]
digits[:len(INPUT)] = [int(v) for v in INPUT]
data = create_array(digits)
v = initial_v
for n in range(10**7):
    v = cycle(data, v)
print data[1] * data[data[1]]
