RIGHT = 1
LEFT = 2

class Ant:
    def __init__(self):
        self.pos = (0, 0)
        self.dir = (0, 1)
        self.visited = {(0, 0)}
        self.dup = None

    def step(self, rotation, steps):
        if rotation == LEFT:
            self.dir = (-self.dir[1], self.dir[0])
        elif rotation == RIGHT:
            self.dir = (self.dir[1], -self.dir[0])
        pos = self.pos
        for i in xrange(1, steps + 1):
            pos = (pos[0] + self.dir[0], pos[1] + self.dir[1])
            if self.dup is None:
                self.dup = pos if pos in self.visited else None
                self.visited.add(pos)
        self.pos = pos

def l1_norm(pos):
    return abs(pos[0]) + abs(pos[1])

def parse(str_in):
    result = []
    i = 0
    while i < len(str_in):
        rot = LEFT if str_in[i] == 'L' else RIGHT
        i += 1
        char = str_in[i]
        steps = 0
        while (ord(char) >= 0x30 and ord(char) <= 0x39):
            steps *= 10
            steps += int(char)
            i += 1
            if i >= len(str_in):
                break
            char = str_in[i]
        result.append((rot, steps))
        i += 2 #skip command and space
    return result


INPUT = "R3, R1, R4, L4, R3, R1, R1, L3, L5, L5, L3, R1, R4, L2, L1, R3, L3, R2, R1, R1, L5, L2, L1, R2, L4, R1, L2, L4, R2, R2, L2, L4, L3, R1, R4, R3, L1, R1, L5, R4, L2, R185, L2, R4, R49, L3, L4, R5, R1, R1, L1, L1, R2, L1, L4, R4, R5, R4, L3, L5, R1, R71, L1, R1, R186, L5, L2, R5, R4, R1, L5, L2, R3, R2, R5, R5, R4, R1, R4, R2, L1, R4, L1, L4, L5, L4, R4, R5, R1, L2, L4, L1, L5, L3, L5, R2, L5, R4, L4, R3, R3, R1, R4, L1, L2, R2, L1, R4, R2, R2, R5, R2, R5, L1, R1, L4, R5, R4, R2, R4, L5, R3, R2, R5, R3, L3, L5, L4, L3, L2, L2, R3, R2, L1, L1, L5, R1, L3, R3, R4, R5, L3, L5, R1, L3, L5, L5, L2, R1, L3, L1, L3, R4, L1, R3, L2, L2, R3, R3, R4, R4, R1, L4, R1, L5"

instructions = parse("R8, R4, R4, R8")
instructions = parse(INPUT)
ant = Ant()
positions = {(0, 0)}
dup = None
for s in instructions:
    ant.step(s[0], s[1])
print l1_norm(ant.pos)
print l1_norm(ant.dup)
