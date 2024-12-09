"""
Not the most sophisticated solution.
Part 1 we just swap values around with two iterators; one walking forwards
looking for empty spaces and one walking backwards looking for values.

For Part 2, we have a list of (value, length) and just do the O(n^2) walk.
It's not fast, but not slow enough for me to want to write some linked list
structure that might be a bit more efficient (~5 seconds).
"""


def parse_line(line):
    return list(map(int, (s for s in line)))

def parse_file(filename):
    with open(filename) as f:
        return parse_line(next(f).strip())


def expand_data(data):
    expanded = []
    gap = False
    file_id = 0
    for d in data:
        for _ in range(d):
            expanded.append(file_id if not gap else None)
        if gap:
            file_id += 1
        gap = not gap
    return expanded


def compact(expanded):
    left, right = 0, len(expanded) - 1
    def forward():
        nonlocal left
        nonlocal right
        nonlocal expanded
        while True:
            if left > right:
                return
            while expanded[left] is not None:
                left += 1
                if left > right:
                    return
            yield left

    def backward():
        nonlocal left
        nonlocal right
        nonlocal expanded
        while True:
            if right < left:
                return
            while expanded[right] is None:
                right -= 1
                if right < left:
                    return
            yield right

    for l, r in zip(forward(), backward()):
        expanded[l] = expanded[r]
        expanded[r] = None
    return expanded


def checksum(expanded):
    s = 0
    for n, file_id in enumerate(expanded):
        s += n * file_id if file_id else 0
    return s


def expand_rle(data):
    expanded = []
    file_id = 0
    is_value = True
    for d in data:
        expanded.append((file_id if is_value else None, d))
        if is_value:
            file_id += 1
        is_value = not is_value
    return expanded


def compact_whole(expanded):
    processed = 0x7FFFFFFF
    right = len(expanded) - 1
    while right:
        if expanded[right][0] is None:
            right -= 1
        elif expanded[right][0] >= processed:
            right -= 1
        else:
            left = 0
            processed = expanded[right][0]
            while left < right:
                if expanded[left][0] is not None:
                    left += 1
                elif expanded[left][1] < expanded[right][1]:
                    left += 1
                else:
                    diff = expanded[left][1] - expanded[right][1]
                    expanded[left] = expanded[right]
                    expanded[right] = (None, expanded[right][1])
                    if diff:
                        expanded.insert(left + 1, (None, diff))
                        right += 1
                    break
    return expanded


def checksum_rle(expanded):
    s = 0
    l_idx = None
    r_idx = 0
    for v, l in expanded:
        l_idx = r_idx
        r_idx += l
        if v is not None:
            c1 = (r_idx * (r_idx - 1)) // 2
            c2 = (l_idx * (l_idx - 1)) // 2
            s += v * (c1-c2)
    return s


test_data = "2333133121414131402"
#test_data = "12345"
data = parse_file("09.txt")
#data = parse_line(test_data)
expanded = expand_data(data)
expanded = compact(expanded)
print(checksum(expanded))

expanded = expand_rle(data)
expanded = compact_whole(expanded)
print(checksum_rle(expanded))
