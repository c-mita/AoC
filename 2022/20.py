"""
Do the simple thing; a doubly linked list and a map of values into
nodes in the list. Shifting things modulo the length of the list
is "quick enough", but it's not great...

Part 2 about 10 seconds.
"""


def parse_file(filename):
    with open(filename) as f:
        return [int(line.strip()) for line in f]


class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

    def insert_right(self, value):
        right = Node(value)
        return self.link_right(right)

    def link_right(self, right):
        if self.right:
            right.right = self.right
            self.right.left = right
        right.left = self
        self.right = right
        return right

    def unlink(self):
        self.left.right = self.right
        self.right.left = self.left
        l = self.left
        self.left = None
        self.right = None
        return l

    def swap(self, other):
        left = self.unlink()
        other_left = other.unlink()
        other_left.link_right(self)
        return left.link_right(other)

    def shift(self, n):
        if n == 0:
            return self
        ptr = self.unlink()
        if n > 0:
            while n != 0:
                ptr = ptr.right
                n -= 1
        else:
            while n != 0:
                ptr = ptr.left
                n += 1
        ptr.link_right(self)

    def to_list(self):
        seen = set()
        values = []
        ptr = self
        while ptr not in seen:
            values.append(ptr.value)
            seen.add(ptr)
            ptr = ptr.right
        return values


def create_chain(numbers):
    head = Node(numbers[0])
    zero = None
    ptr = head
    idx_to_node = {0:head}
    for n, v in enumerate(numbers[1:]):
        n += 1
        ptr = ptr.insert_right(v)
        if v == 0:
            zero = ptr
        idx_to_node[n] = ptr
    ptr.link_right(head)
    return zero, idx_to_node


def mix(numbers, times=1):
    zero, idx_to_node = create_chain(numbers)
    # subtract one because when shifting our list is a little shorter
    m = len(numbers) - 1
    for _ in range(times):
        for n, v in enumerate(numbers):
            if v < 0:
                q = -(-v % m)
            else:
                q = v % m
            ptr = idx_to_node[n]
            ptr.shift(q)
    return zero.to_list()


test_numbers = [1, 2, -3, 3, -2, 0, 4]
numbers = parse_file("20_input.txt")
mixed = mix(numbers)
l = len(mixed)
v1, v2, v3 = mixed[1000 % l], mixed[2000 % l], mixed[3000 % l]
s = v1 + v2 + v3
print(v1, v2, v3)
print(s)

numbers = [n * 811589153 for n in numbers]
fully_mixed = mix(numbers, 10)
v1, v2, v3 = fully_mixed[1000 % l], fully_mixed[2000 % l], fully_mixed[3000 % l]
s = v1 + v2 + v3
print(s)
