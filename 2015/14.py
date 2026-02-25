def parse_input(filename):
    data = {}
    with open(filename) as f:
        for line in f:
            elts = line.strip().split(" ")
            name = elts[0]
            speed, duration, rest = map(int, (elts[3], elts[6], elts[-2]))
            data[name] = (speed, duration, rest)
    return data


def distance_travelled(deer_properties, time):
    speed, duration, rest = deer_properties
    full_cycle = duration + rest
    full_cycle_distance = speed * duration
    cycles = int(time // full_cycle)
    remainder = time % full_cycle
    final_run = min(remainder, duration)
    return cycles * full_cycle_distance + final_run * speed


def simulate_race(deers):
    def travel_distance(properties, time):
        speed, duration, rest = properties
        full_cycle = duration + rest
        remainder = time % full_cycle
        if remainder < duration:
            return speed
        return 0

    distances = {d:0 for d in deers}
    scores = {d:0 for d in deers}
    for t in range(2503):
        for deer in deers:
            d = travel_distance(deers[deer], t)
            distances[deer] += d
        current_distances = sorted([(distances[deer], deer) for deer in deers])
        lead_distance = current_distances[-1][0]
        while current_distances and lead_distance == current_distances[-1][0]:
            _distance, deer = current_distances.pop()
            scores[deer] += 1
    return scores


deers = parse_input("14.txt")
distances = (distance_travelled(deers[d], 2503) for d in deers)
print(max(distances))

scores = simulate_race(deers)
print(max(scores.values()))
