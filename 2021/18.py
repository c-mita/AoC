import math

# It may actually be easier to solve this problem by acting on the textual input
# to perform some of the reductions, rather than constructing graph objects; the
# explode operation is quite awkward.
# Calculating the magnitude is easy though.
#
# Not so efficient, but fast enough to satisfy me (~2 seconds for Part 2)


def parse_file(filename):
    with open(filename) as f:
        return [parse_number(line.strip()) for line in f]

def parse_number(string):
    builder = SnailBuilder()
    for c in string.strip():
        if c == " ":
            continue
        builder.add(c)
    return builder.build()


class RegularNumber:
    def __init__(self, value):
        self.value = value
        self.finished = True

    def split(self):
        if self.value >= 10:
            left = RegularNumber(math.floor(self.value / 2.))
            right = RegularNumber(math.ceil(self.value / 2.))
            return SnailNumber(left, right), True
        return RegularNumber(self.value), False

    def magnitude(self):
        return self.value

    def _explode(self, depth=None, exploded=False):
        return self, None, None, exploded

    def __repr__(self):
        return "RegularNumber(%d)" % self.value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other


class SnailNumber:
    def __init__(self, left, right):
        self.left = left
        self.right = right


    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def add_to_leftmost_right(self, value):
        def _recurse(node, value):
            if type(node) == RegularNumber:
                return RegularNumber(node.value + value)
            left = _recurse(node.left, value)
            return SnailNumber(left, node.right)
        return _recurse(self.right, value)

    def add_to_rightmost_left(self, value):
        def _recurse(node, value):
            if type(node) == RegularNumber:
                return RegularNumber(node.value + value)
            right = _recurse(node.right, value)
            return SnailNumber(node.left, right)
        return _recurse(self.left, value)

    def split(self):
        left, split = self.left.split()
        right = self.right
        if not split:
            right, split = self.right.split()
        return SnailNumber(left, right), split

    def explode(self):
        result, _left, _right, exploded = self._explode(depth = 0, exploded=False)
        return result, exploded

    def _explode(self, depth=0, exploded=False):
        if exploded:
            return self, None, None, True
        if depth == 4:
            if not (type(self.left) == RegularNumber and type(self.right) == RegularNumber):
                raise ValueError("Exploding non regular numbers %s" % str((self.left, self.right)))
            return RegularNumber(0), self.left.value, self.right.value, True

        new_left, left, right, exploded = self.left._explode(depth+1, exploded)
        if exploded:
            new_right = self.add_to_leftmost_right(right) if right else self.right
            return SnailNumber(new_left, new_right), left, None, exploded

        new_right, left, right, exploded = self.right._explode(depth+1, exploded)
        if exploded:
            new_left = self.add_to_rightmost_left(left) if left else self.left
            return SnailNumber(new_left, new_right), None, right, exploded

        # No explosioning happened
        return SnailNumber(self.left, self.right), None, None, exploded


    def add(self, other):
        added = SnailNumber(self, other)
        changed = True
        while changed:
            added, explodes = added.explode()
            while explodes:
                added, explodes = added.explode()
            split, splits = added.split()
            added = split
            changed = explodes or splits
        return added

    def __str__(self):
        return "[%s, %s]" % (self.left, self.right)

    def __repr__(self):
        return "SnailNumber(%s, %s)" % (repr(self.left), repr(self.right))

    def __eq__(self, other):
        if not type(other) == SnailNumber:
            return False
        return self.left == other.left and self.right == other.right


class SnailBuilder:
    def __init__(self):
        self.left = None
        self.right = None
        self.started = None
        self.finished = False

    def add(self, c):
        if self.finished:
            raise ValueError("Adding to finished number")

        if not self.left:
            if c == "[":
                # the outermost Builder needs to parse the first "[" without
                # recursing down
                if not self.started:
                    self.started = True
                else:
                    self.left = SnailBuilder()
                    self.left.started = True
            else:
                self.left = RegularNumber(int(c))
        elif not self.left.finished:
            self.left.add(c)
        elif c == ",":
            if not self.left.finished:
                raise ValueError("Comma when left side not complete")
        elif not self.right:
            if c == "[":
                self.right = SnailBuilder()
                self.right.started = True
            else:
                self.right = RegularNumber(int(c))
        elif not self.right.finished:
            self.right.add(c)
        elif c == "]":
            self.finished = True
        else:
            raise ValueError("Unrecognised state")

    def build(self):
        if not self.finished:
            raise ValueError("Cannot build incomplete SnailNumber")
        left = self.left.build() if type(self.left) == SnailBuilder else self.left
        right = self.right.build() if type(self.right) == SnailBuilder else self.right
        return SnailNumber(left, right)

    def __str__(self):
        return "[%s, %s]" % (self.left, self.right)



snail_numbers = parse_file("18_input.txt")

summed = snail_numbers[0]
for snail in snail_numbers[1:]:
    summed = summed.add(snail)
print(summed.magnitude())


print(max(s1.add(s2).magnitude() for s1 in snail_numbers for s2 in snail_numbers if s1 != s2))
