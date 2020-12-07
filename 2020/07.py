import re


def parse_line(line):
    line = line.strip().strip(".")
    bag, contains = line.split(" bags contain ")
    if "no other" in contains:
        return bag, []
    bags = contains.split(", ")
    colours = [v.strip() for v in re.split("bags|bag|[0-9]|,", contains) if v.strip()]
    counts = [int(v) for v in re.findall("[0-9]*", contains) if v.strip()]
    return bag, list(zip(colours, counts))


def parse_file(filename):
    with open(filename) as f:
        return dict(parse_line(l) for l in f)


def invert_map(mapping):
    d = {c:set() for c in mapping}
    for k, v in mapping.items():
        for colour, n in v:
            d[colour].add(k)
    return d


def traverse_for_colour_count(colour, inverse_map):
    parent_colours = set()
    for parent in inverse_map[colour]:
        parent_colours.add(parent)
        parent_colours.update(traverse_for_colour_count(parent, inverse_map))
    return parent_colours


def traverse_for_bag_count(colour, forward_map):
    n = 0
    for c, v in forward_map[colour]:
        v2 = traverse_for_bag_count(c, forward_map)
        n += v * v2 + v
    return n


forward_map = parse_file("07.txt")
inverse_map = invert_map(forward_map)
print len(traverse_for_colour_count("shiny gold", inverse_map))
print traverse_for_bag_count("shiny gold", forward_map)
