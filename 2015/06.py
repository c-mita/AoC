import re


"""
I could be clever solving this by tracking rectangles and splitting them
on overlaps. But I'm doing this in an aeroplane and I cannot be bothered.
"""

def parse_input(filename):
    data = []
    with open(filename) as f:
        for line in f:
            if line.startswith("toggle"):
                op = "toggle"
            elif line.startswith("turn on"):
                op = "on"
            elif line.startswith("turn off"):
                op = "off"
            else:
                raise ValueError("Cannot parse '%s'" % line)
            sx, sy, ex, ey = map(int, re.findall("[0-9]+", line))
            data.append((op, (sx, sy), (ex, ey)))
    return data


def is_on(light, instructions):
    def _rec(px, py, idx):
        while idx >= 0:
            op, (sx, sy), (ex, ey) = instructions[idx]
            idx -= 1
            if not (sx <= px <= ex and sy <= py <= ey):
                continue
            if op == "on":
                return True
            elif op == "off":
                return False
            elif op == "toggle":
                return not _rec(px, py, idx)
            else:
                raise ValueError("Bad op '%s'" % op)
        return False

    return _rec(light[0], light[1], len(instructions)-1)


def process_instructions(instructions):
    coords = ((x, y) for x in range(1000) for y in range(1000))
    lights = {l:0 for l in coords}
    for instruction in instructions:
        op, (sx, sy), (ex, ey) = instruction
        coords = ((x, y) for x in range(sx, ex+1) for y in range(sy, ey+1))
        for x, y in coords:
            if op == "on":
                lights[(x, y)] += 1
            elif op == "toggle":
                lights[(x, y)] += 2
            elif op == "off":
                lights[(x, y)] = max(lights[(x, y)] - 1, 0)
    return lights



data = parse_input("06.txt")
lights = [(x, y) for x in range(1000) for y in range(1000)]
lit = [l for l in lights if is_on(l, data)]
print(len(lit))

lights = process_instructions(data)
brightness = sum(lights.values())
print(brightness)
