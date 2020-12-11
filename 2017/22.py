def turn_left(pos):
    x, y = pos
    return (y, -x)


def turn_right(pos):
    x, y = pos
    return (-y, x)


def turn_back(pos):
    x, y = pos
    return (-x, -y)


def parse_file(filename):
    infected = set()
    with open(filename) as f:
        for j, l in enumerate(f):
            for i, c in enumerate(l.strip()):
                if c == "#":
                    infected.add((i, j))
        return (i/2, j/2), infected


def cycle(infected, position, direction):
    new_infected = False
    if position in infected:
        direction = turn_right(direction)
        infected.remove(position)
    else:
        direction = turn_left(direction)
        infected.add(position)
        new_infected = True
    position = (position[0] + direction[0], position[1] + direction[1])
    return position, direction, new_infected


def evolved_cycle(states, position, direction):
    new_infected = False
    if position not in states:
        direction = turn_left(direction)
        states[position] = "W"
    else:
        state = states[position]
        if state == "W":
            states[position] = "I"
            new_infected = True
        elif state == "I":
            states[position] = "F"
            direction = turn_right(direction)
        elif state == "F":
            del states[position]
            direction = turn_back(direction)
    position = (position[0] + direction[0], position[1] + direction[1])
    return position, direction, new_infected


initial_position, initial_infected = parse_file("22_input.txt")
initial_direction = (0, -1)

position = initial_position
direction = initial_direction
infected = set(initial_infected)
c = 0
for n in range(10000):
    position, direction, new = cycle(infected, position, direction)
    if new: c += 1
print c


states = {k:"I" for k in initial_infected}
position = initial_position
direction = initial_direction
c = 0
for n in range(10000000):
    position, direction, new = evolved_cycle(states, position, direction)
    if new: c += 1
print c
