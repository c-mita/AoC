import collections

def parse_file(filename):
    with open(filename) as f:
        data = f.readline().strip()
    return data

def find_marker_start(data, unique_length):
    chain = collections.deque("0" * unique_length)
    current = collections.Counter()
    for n, d in enumerate(data):
        current[chain.popleft()] -= 1
        current[d] += 1
        chain.append(d)
        if len(set(current.elements())) == unique_length:
            return n + 1 # answer expects one based indexing
    raise ValueError("No %d length sequence of unique characters" % unique_length)



data = parse_file("06_input.txt")
start_marker = find_marker_start(data, 4)
print(start_marker)

message_start = find_marker_start(data, 14)
print(message_start)
