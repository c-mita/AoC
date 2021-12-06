import collections

def parse_file(filename):
    with open(filename) as f:
        line = f.readlines()[0].strip()
        return map(int, line.split(","))


def run_for_steps(state, steps):
    state = list(state)
    for n in range(steps):
        for idx in range(len(state)):
            if state[idx] == 0:
                state[idx] = 6
                state.append(8)
            else:
                state[idx] -= 1
    return state


def calculate_for_steps(state, steps):
    # we try to track how many we're going to have/add on a given day
    to_add = collections.defaultdict(int)
    count = len(state)
    for starting_day in state:
        for day in range(starting_day, steps, 7):
            to_add[day] += 1

    for day in range(steps):
        spawned = to_add[day]
        count += spawned
        if spawned:
            for spawning_day in range(day + 9, steps, 7):
                to_add[spawning_day] += spawned
    return count



test_input = [3, 4, 3, 1, 2]
start = parse_file("06_input.txt")
#end = run_for_steps(start, 80)
#print len(end)
print(calculate_for_steps(start, 80))

result = calculate_for_steps(start, 256)
print(result)
