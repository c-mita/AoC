def parse_file(filename):
    trees = {}
    with open(filename) as f:
        for r, line in enumerate(f):
            for c, v in enumerate(line.strip()):
                trees[(r, c)] = int(v)
    return trees, (r, c)


def mark_visible(trees, max_r, max_c):
    def run_sequence(start, increment):
        visible = set()
        height = -1
        pos = start
        while pos in trees:
            if trees[pos] > height:
                visible.add(pos)
                height = trees[pos]
            pos = (pos[0] + increment[0], pos[1] + increment[1])
        return visible

    visible = set()
    for r in range(max_r+1):
        visible |= run_sequence((r, 0), (0, 1))
        visible |= run_sequence((r, max_c), (0, -1))
    for c in range(max_c+1):
        visible |= run_sequence((0, c), (1, 0))
        visible |= run_sequence((max_r, c), (-1, 0))
    return visible


def sight_scores(trees, max_r, max_c):
    # this is not a clever solution, but the scale of the problem is not
    # high enough to punish it.
    scores = {}
    def check_direction(start, increment):
        count = 0
        height = trees[start]
        pos = start[0] + increment[0], start[1] + increment[1]
        while pos in trees:
            count += 1
            if trees[pos] >= height:
                break
            pos = pos[0] + increment[0], pos[1] + increment[1]
        return count
    for tree in trees:
        p = 1
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            p *= check_direction(tree, direction)
        scores[tree] = p
    return scores


trees, (max_r, max_c) = parse_file("08_input.txt")
# Part 1
visible = mark_visible(trees, max_r, max_c)
print(len(visible))

# Part 2
scores = sight_scores(trees, max_r, max_c)
print(max(scores.values()))
