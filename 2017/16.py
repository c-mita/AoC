def spin(positions, n):
    pivot = len(positions) - n
    l = positions[pivot:]
    positions[n:] = positions[:pivot]
    positions[:n] = l

def exchange(positions, a, b):
    positions[a], positions[b] = positions[b], positions[a]

def partner(positions, a, b):
    a, b = positions.index(a), positions.index(b)
    positions[a], positions[b] = positions[b], positions[a]

def parse_input(filename):
    def parse_command(cmd):
        cmd = cmd.strip()
        if cmd[0] == 's':
            return (spin, (int(cmd[1:]),))
        elif cmd[0] == 'x':
            return (exchange, tuple(int(d) for d in cmd[1:].split("/")))
        elif cmd[0] == 'p':
            return (partner, tuple(cmd[1:].split("/")))

    with open(filename) as f:
        return [parse_command(cmd) for cmd in f.readline().split(",")]

l = [chr(c + 0x61) for c in xrange(16)]
commands = parse_input("16_input.txt")
for func, args in commands:
    func(l, *args)
print "".join(l)

n = 0
l = [chr(c + 0x61) for c in xrange(16)]
seen = {}
target = 10**9
while n < target:
    p = "".join(l)
    if p in seen: break
    else: seen[p] = n
    n += 1
    for func, args in commands:
        func(l, *args)

if not n == target:
    cycle = n - seen[p]
    cycles_needed = (target - seen[p]) / cycle
    remaining = (target - seen[p]) % cycle
    for i in xrange(remaining):
        for func, args in commands:
            func(l, *args)
    p = "".join(l)
print p

