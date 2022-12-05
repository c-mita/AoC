import collections
import re

Move = collections.namedtuple("Move", ["number", "source", "target"])

# Part 1 can be solved efficiently with collections.deque
# Part 2 can be solved "good enough"ly with lists and slicing but we want
# the nerd points that come with a linked list implementation.

class Node:
    def __init__(self, value):
        self.next = None
        self.prev = None
        self.value = value

    def link_before(self, node):
        self.next = node
        node.prev = self

    def detach_before(self):
        if self.prev:
            self.prev.next = None
            self.prev = None


class DLinkedList():
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = self.tail = new_node
            return
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node

    def appendleft(self, value):
        new_node = Node(value)
        if not self.tail:
            self.head = self.tail = new_node
            return
        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node

    def pop(self):
        if self.tail is None:
            raise IndexError("No elements in linked list")
        node = self.tail
        self.tail = node.prev
        node.detach_before()
        if self.head == node:
            self.head = None
        return node.value

    def peek(self):
        if self.tail is None:
            raise IndexError("No elements in linked list")
        return self.tail.value

    def detach_from_right(self, number):
        new_list = DLinkedList()
        new_list.tail = self.tail
        node = self.tail
        for _ in range(number-1):
            node = node.prev
        self.tail = node.prev
        if self.tail is None:
            self.head = None
        node.detach_before()
        new_list.head = node
        return new_list

    def attach(self, linked_list):
        if self.tail is None:
            self.head = linked_list.head
            self.tail = linked_list.tail
        else:
            self.tail.link_before(linked_list.head)
            self.tail = linked_list.tail


def parse_file(filename):
    moves = []
    stacks = collections.defaultdict(DLinkedList)
    with open(filename) as f:
        line = next(f)
        while "1" not in line:
            for n, c in enumerate(line[1::4]):
                if c.strip():
                    stacks[n+1].appendleft(c)
            line = next(f)
        next(f) # empty line
        for line in f:
            moves.append(Move(*map(int, re.findall("[0-9]+", line))))
    return stacks, moves


def apply_move_single(stacks, move):
    number, source, target = move
    for _ in range(number):
        stacks[target].append(stacks[source].pop())

def apply_move_multiple(stacks, move):
    number, source, target = move
    stacks[target].attach(stacks[source].detach_from_right(number))

# Part 1
stacks, moves = parse_file("05_input.txt")
for move in moves:
    apply_move_single(stacks, move)
top_crates = "".join(stacks[n+1].peek() for n in range(len(stacks)))
print(top_crates)

# Part 2
stacks, moves = parse_file("05_input.txt")
for move in moves:
    apply_move_multiple(stacks, move)
top_crates = "".join(stacks[n+1].peek() for n in range(len(stacks)))
print(top_crates)
