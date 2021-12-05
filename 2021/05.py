import collections

def parse_input(filename):
    segments = []
    with open(filename) as f:
        for line in f:
            first, second = line.strip().split(" -> ")
            first = map(int, first.split(","))
            second = map(int, second.split(","))
            segments.append((first, second))
    return segments

def aligned_segments(segments):
    aligned = []
    for (p1x, p1y), (p2x, p2y) in segments:
        if p1x == p2x or p1y == p2y:
            aligned.append(((p1x, p1y), (p2x, p2y)))
    return aligned

def apply_segments(segments):
    points = collections.defaultdict(int)
    for (p1x, p1y), (p2x, p2y) in segments:
        dx, dy = p2x - p1x, p2y - p1y
        if dx: dx /= abs(dx)
        if dy: dy /= abs(dy)
        px, py = p1x, p1y
        points[(px, py)] += 1
        while (px, py) != (p2x, p2y):
            px += dx
            py += dy
            points[(px, py)] += 1
    return points

segments = parse_input("05_input.txt")
aligned = aligned_segments(segments)
hit = apply_segments(aligned)
print sum(1 for p in hit if hit[p] > 1)
hit = apply_segments(segments)
print sum(1 for p in hit if hit[p] > 1)
