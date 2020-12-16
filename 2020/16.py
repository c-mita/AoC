import re


def parse_values(line):
    return map(int, line.strip().split(","))


def parse_ranges(line):
    name, ranges = line.split(": ")
    values = re.findall("[0-9]+", ranges)
    range_values = [(int(v1), int(v2)) for (v1, v2) in zip(values[::2], values[1::2])]
    return name, range_values


def parse_file(filename):
    with open(filename) as f:
        data = f.read()
        b1, b2, b3 = data.split("\n\n")

        ranges = dict(parse_ranges(l) for l in b1.split("\n"))
        ticket = parse_values(b2.split("\n")[1])
        tickets = [parse_values(l) for l in b3.split("\n")[1:-1]]

        return ticket, ranges, tickets


def filter_tickets(tickets, ranges):
    error_sum = 0
    valid_tickets = []
    for ticket in tickets:
        valid_t = True
        for v in ticket:
            valid_v = False
            for bounds in ranges.values():
                for l, u in bounds:
                    if l <= v <= u:
                        valid_v = True
            if not valid_v:
                error_sum += v
                valid_t = False
        if valid_t:
            valid_tickets.append(ticket)
    return error_sum, valid_tickets


def check_bounds_fit(ticket_values, bounds):
    (l1, u1), (l2, u2) = bounds
    for v in ticket_values:
        if l1 <= v <= u1:
            continue
        if l2 <= v <= u2:
            continue
        return False
    return True


def foo(bounds_map, indexes=None, key_set=set()):
    if indexes is None:
        # it is much quicker to trial indexes in order of number of possiblities
        # there are some that only have one option, which restricts another with only two
        # optons, etc.
        indexes = sorted(range(len(tickets_rotated)), key=lambda n: len(index_map[n]))
    if not indexes:
        return []

    index = indexes[0]
    for k in index_map[index] - key_set:
        try:
            return [(index, k)] + foo(bounds_map, indexes[1:], key_set=key_set | set([k]))
        except ValueError:
            continue
    raise ValueError("Exhausted keys")



tickets = [[7,3,47],[40,4,50],[55,2,20],[38,6,12]]
ranges = {"class":[(1,3),(5,7)], "row":[(6,11),(33,44)], "seat":[(13,40),(45,50)]}
ticket, ranges, tickets = parse_file("16.txt")

error_sum, valid_tickets = filter_tickets(tickets, ranges)
print error_sum

tickets_rotated = [[t[n] for t in valid_tickets] for n in range(len(valid_tickets[0]))]
bounds_map = {key : set(n for n,t in enumerate(tickets_rotated) if check_bounds_fit(t, ranges[key])) for key in ranges}
index_map = {n : set(key for key in ranges if check_bounds_fit(t, ranges[key])) for (n, t) in enumerate(tickets_rotated)}

idx_key_map = dict(foo(index_map))
p = 1
for n, v in enumerate(ticket):
    if idx_key_map[n][:9] == "departure":
        p *= v
print p
