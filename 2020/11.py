class ImmediateNeighbourRule:
    def __init__(self, seats):
        self.neighbours = {}
        for (ky, kx) in seats.keys():
            neighbours = [
                    (ky-1, kx-1), (ky-1, kx), (ky-1, kx+1),
                    (ky, kx-1), (ky, kx+1),
                    (ky+1, kx-1), (ky+1, kx), (ky+1, kx+1)]
            self.neighbours[(ky, kx)] = [n for n in neighbours if n in seats]

    def __call__(self, key, seats):
        return sum(seats[n] for n in self.neighbours[key])



class VisibleNeighbourRule:
    def __init__(self, seats):
        self.neighbours = {}
        y_max = max(k[0] for k in seats)
        x_max = max(k[1] for k in seats)
        for (ky, kx) in seats.keys():
            u = [(y, kx) for y in range(ky-1, -1, -1)]
            d = [(y, kx) for y in range(ky+1, y_max+1)]
            l = [(ky, x) for x in range(kx-1, -1, -1)]
            r = [(ky, x) for x in range(kx+1, x_max+1)]
            rd = [(y, x) for y, x in zip(range(ky+1, y_max+1), range(kx+1, x_max+1))]
            ld = [(y, x) for y, x in zip(range(ky+1, y_max+1), range(kx-1, -1, -1))]
            ru = [(y, x) for y, x in zip(range(ky-1, -1, -1), range(kx+1, x_max+1))]
            lu = [(y, x) for y, x in zip(range(ky-1, -1, -1), range(kx-1, -1, -1))]
            sets = [u, d, l, r, rd, ld, ru, lu]
            self.neighbours[(ky, kx)]  = []
            for s in sets:
                matched = [t for t in s  if t in seats]
                if matched: self.neighbours[(ky, kx)].append(matched[0])


    def __call__(self, key, seats):
        return sum(seats[n] for n in self.neighbours[key])



def parse_file(filename):
    indices = []
    with open(filename) as f:
        for i, l in enumerate(f):
            for j, c in enumerate(l.strip()):
                if c != ".":
                    indices.append((i, j))
    return indices


def cycle(seats, rule, tolerance):
    next_seats = {}
    changed = False
    for k, v in seats.items():
        next_seats[k] = v
        nc = rule(k, seats)
        if nc == 0:
            next_seats[k] = 1
        elif nc >= tolerance:
            next_seats[k] = 0
        changed |= next_seats[k] != v
    return changed, next_seats



seats = parse_file("11.txt")
seat_map = {k:0 for k in seats}
close_rule = ImmediateNeighbourRule(seat_map)
n = 0
changed = True
while changed:
    changed, seat_map = cycle(seat_map, close_rule, 4)
    n += 1
print sum(v for v in seat_map.values())

seat_map = {k:0 for k in seats}
visible_rule = VisibleNeighbourRule(seat_map)
n = 0
changed = True
while changed:
    changed, seat_map = cycle(seat_map, visible_rule, 5)
    n += 1
print sum(v for v in seat_map.values())
