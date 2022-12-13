import re


def parse_file(filename):
    pairs = []
    with open(filename) as f:
        try:
            while True:
                first = next(f).strip()
                second = next(f).strip()
                pairs.append((first, second))
                _ = next(f)
        except StopIteration:
            pass
    return pairs


class NestedNumber:
    def __init__(self, values):
        self.values = values

    def cmp(self, other):
        if type(other) != NestedNumber:
            return self.cmp(NestedNumber([other]))
        i1 = -1
        i2 = -1
        for (i1, v1), (i2, v2) in zip(enumerate(self.values), enumerate(other.values)):
            if v1 < v2:
                return -1
            if v1 > v2:
                return 1
        if i1 < len(self.values) - 1:
            return 1
        if i2 < len(other.values) - 1:
            return -1
        return 0

    def __lt__(self, other):
        return self.cmp(other) == -1

    def __gt__(self, other):
        return self.cmp(other) == 1

    def __le__(self, other):
        return not self.cmp(other) == 1

    def __ge__(self, other):
        return not self.cmp(other) == -1

    def __str__(self):
        return "%s" % self.values

    def __repr__(self):
        return "NestedNumber(%s)" % self.values


def parse_nested_number(text):
    def _rec(symbols):
        values = []
        while True:
            try:
                c = next(symbols)
                if c == "]":
                    return NestedNumber(values)
                if c == "[":
                    values.append(_rec(symbols))
                else:
                    values.append(int(c))
            except StopIteration:
                return NestedNumber(values)
    symbols = iter(re.findall("\[|\]|[0-9]+", text))
    return _rec(symbols)


pairs = parse_file("13_input.txt")
nn_pairs = [(parse_nested_number(l), parse_nested_number(r)) for (l, r) in pairs]

# Part 1
in_order = []
for n, (l, r) in enumerate(nn_pairs):
    if l <= r:
        in_order.append(n+1)
print(sum(in_order))

# Part 2
# Since we have the comparison operations defined already, we can just sort
# the list of packets and then scan looking for our marker packets.
packets = []
for p in nn_pairs:
    packets.append(p[0])
    packets.append(p[1])
marker_1 = parse_nested_number("[[2]]")
marker_2 = parse_nested_number("[[6]]")
packets.append(marker_1)
packets.append(marker_2)

sorted_packets = sorted(packets)
idx_1 = sorted_packets.index(marker_1)
idx_2 = sorted_packets.index(marker_2)
print((idx_1 + 1) * (idx_2 + 1))
