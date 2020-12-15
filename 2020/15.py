TEST_INPUT = [0, 3, 6]
INPUT = [0, 14, 1, 3, 7, 9]



def speak_numbers(numbers):
    if not numbers: raise ValueError("No numbers!")
    spoken = {}
    for (n, v) in enumerate(numbers):
        yield v
        spoken[v] = n+1
    last = v

    while True:
        n += 1
        v = n - spoken[last] if v in spoken else 0
        spoken[last] = n
        yield v
        last = v


def speak_numbers_limit(numbers, limit):
    # this is a little faster than the dict, 15s->5s on a weak laptop
    spoken = [0] * limit
    for (n, v) in enumerate(numbers):
        yield v
        spoken[v] = n+1
    last = v

    while n < limit-1:
        n += 1
        v = n - spoken[last] if spoken[v] else 0
        spoken[last] = n
        yield v
        last = v


for n, v in zip(range(2020), speak_numbers(INPUT)):
    pass
print v

for v in speak_numbers_limit(INPUT, 30000000):
    pass
print v
