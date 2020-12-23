class Node:
    def __init__(self, value):
        self.fwrd = self
        self.back = self
        self.value = value


    def unlink(self):
        self.fwrd.back = self.back
        self.back.fwrd = self.fwrd
        return self.fwrd


    def link(self, node):
        node.fwrd = self.fwrd
        node.fwrd.back = node
        self.fwrd = node
        node.back = self
        return node


    def insert(self, value):
        """Adds a node after the current node and returns it."""
        node = Node(value)
        return self.link(node)


def create_circle(digit_str):
    digits = map(int, (s for s in digit_str))
    pointers = [None] * max(digits)
    circle = Node(digits[0])
    pointers[digits[0]-1] = circle
    for v in digits[1:]:
        circle = circle.insert(v)
        pointers[v-1] = circle
    return circle.fwrd, pointers


def cycle(circle, pointers):
    n1, n2, n3 = circle.fwrd, circle.fwrd.fwrd, circle.fwrd.fwrd.fwrd
    n1.unlink()
    n2.unlink()
    n3.unlink()
    v1, v2, v3 = n1.value, n2.value, n3.value
    d = circle.value - 1
    min_v, max_v = 1, len(pointers)
    if d < min_v: d = max_v
    while d in [v1, v2, v3]:
        d -= 1
        if d < min_v:
            d = max_v
    node = circle
    node = pointers[d-1]
    node.link(n1).link(n2).link(n3)
    return circle.fwrd


def collect_values(circle):
    values = []
    n = circle
    while n.value != 1:
        n = n.fwrd
    n = n.fwrd
    while n.value != 1:
        values.append(n.value)
        n = n.fwrd
    return "".join(map(str, values))


TEST_INPUT = "389125467"
INPUT = "394618527"

circle, pointers = create_circle(INPUT)
for n in range(100):
    circle = cycle(circle, pointers)
print collect_values(circle)

digits = [n+1 for n in range(10**6)]
digits[:len(INPUT)] = [int(v) for v in INPUT]
circle, pointers = create_circle(digits)
for n in range(10**7):
    circle = cycle(circle, pointers)
node = pointers[0]
print node.fwrd.value * node.fwrd.fwrd.value
