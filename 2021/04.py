def parse_file(filename):
    with open(filename) as f:
        lines = [l.strip() for l in f]
    rng = map(int, lines[0].split(","))

    blocks = []
    current_block = []
    for line in lines[2:]:
        if not line:
            blocks.append(current_block)
            current_block = []
            continue
        current_block.append(map(int, line.strip().split()))
    blocks.append(current_block)
    return rng, blocks


def process_block(block):
    columns = [set() for _ in block]
    rows = []
    for row in block:
        rows.append(set(row))
        for n, v in enumerate(row):
            columns[n].add(v)
    return columns + rows


def find_winning_score(rng, blocks):
    block_units = [process_block(block) for block in blocks]
    winners, scores = run_to_winner(iter(rng), block_units)
    return scores[0]


def run_to_winner(rng, block_units):
    while True:
        r = next(rng)
        winners = []
        scores = []
        for n, units in enumerate(block_units):
            for unit in units:
                if r in unit:
                    unit.remove(r)
                if not unit:
                    winners.append(n)
        if winners:
            # the same index may have been added to winners multiple times
            winners = sorted(set(winners))
            for winner in winners:
                remaining = reduce(lambda s1, s2: s1 | s2, (unit for unit in block_units[winner]))
                scores.append(r * sum(remaining))
            return winners, scores


def find_losing_score(rng, blocks):
    block_units = [process_block(block) for block in blocks]
    rng = iter(rng)
    while len(block_units) > 1:
        winners, scores = run_to_winner(rng, block_units)
        for idx in reversed(winners):
            block_units.pop(idx)
    winners, scores = run_to_winner(rng, block_units)
    return scores[0]


rng, blocks = parse_file("04_input.txt")
print(find_winning_score(rng, blocks))
print(find_losing_score(rng, blocks))
