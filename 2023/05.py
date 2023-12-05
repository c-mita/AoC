"""
Part 1 is straightforward. Take a seed value and run it through the "maps"
in order. For each "map", we sort the mapping tuples by "source" so we
can run through them backwards. This means we know which mapping is relevant
(it's the first once with 'source' < 'value'), assuming we have non-overlapping
mappings.

Part 2 is similar, but operate on intervals instead. This means we sometimes
split intervals when the interval crosses a mapping boundary and map each
interval separately.
"""


def parse_block(block):
    # skip over the name
    mappings = []
    for line in block.split("\n")[1:]:
        line = line.strip()
        if not line:
            continue
        destination, source, length = tuple(map(int, line.split()))
        mappings.append((source, destination, length))
    return sorted(mappings)


def parse_file(filename):
    mappings = []
    with open(filename) as f:
        lines = "".join(l for l in f)
        blocks = lines.split("\n\n")
        seeds = blocks[0]
        seeds = list(map(int, seeds.split(" ")[1:]))
        for block in blocks[1:]:
            mappings.append(parse_block(block))
    return seeds, mappings


def map_number(n, mapping):
    # our mappings are sorted by "source"
    # if we walk them backwards and terminate the first time we find a source
    # value smaller than "n", we can quickly identify the mapped value
    for source, target, length in reversed(mapping):
        if source > n:
            continue
        elif source <= n:
            if n - source <= length:
                return target + (n - source)
            return n
    return n


def run_all_maps(seed, mappings):
    n = seed
    for mapping in mappings:
        n = map_number(n, mapping)
    return n


def map_interval(interval, mapping):
    start, end = interval
    split_intervals = []
    mapped_interval = (start, end)
    for source, target, length in reversed(mapping):
        max_mapped = source + length - 1
        if end < source:
            continue
        if max_mapped < start:
            break
        if start < source:
            split_intervals.append((start, source-1))
            start = source
        if end > max_mapped:
            split_intervals.append((max_mapped + 1, end))
            end = max_mapped
        delta = start - source
        interval_length = end - start
        mapped_interval = (target + delta, target + delta + interval_length)
        break
    mapped = [map_interval(i, mapping) for i in split_intervals]
    mapped = sum(mapped, [])
    mapped.append(mapped_interval)
    return mapped


def run_all_interval_maps(initial, mappings):
    current = [initial]
    for mapping in mappings:
        new_intervals = []
        for interval in current:
            new_intervals.extend(map_interval(interval, mapping))
        current = new_intervals
    return current


seeds, mappings = parse_file("05.txt")
locations = [run_all_maps(seed, mappings) for seed in seeds]
print(min(locations))

seed_intervals = []
for start, length in zip(seeds[:-1:2], seeds[1::2]):
    seed_intervals.append((start, start + length-1))
all_locations = [run_all_interval_maps(interval, mappings) for interval in seed_intervals]
location_intervals = sum(all_locations, [])
print(min(location_intervals)[0])
