def parse_input(filename):
    with open(filename) as f:
        return [l.strip("\n") for l in f]

def follow_path(path):
    markers_seen = []
    pr, pc = 0, path[0].index("|")
    dr, dc = 1, 0 # direction of step increments
    step_count = 1
    end = False
    while not end:
        pr += dr
        pc += dc
        step_count += 1
        symbol = path[pr][pc]
        if symbol == "|" or symbol == "-":
            continue
        elif symbol == "+":
            # check all cardinal directions for a possible route away
            # avoid the one that is the "opposite"
            prev = (dr, dc)
            if (dr, dc) != (0, 1) and path[pr][pc - 1] != " ": dr, dc = 0, -1
            elif (dr, dc) != (0, -1) and path[pr][pc + 1] != " ": dr, dc = 0, 1
            elif (dr, dc) != (1, 0) and path[pr - 1][pc] != " ": dr, dc = -1, 0
            elif (dr, dc) != (-1, 0) and path[pr + 1][pc] != " ": dr, dc = 1, 0
            if prev == (dr, dc):
                end = True
                break
        else:
            markers_seen.append(symbol)
            # check if we're at the end
            if path[pr + dr][pc + dc] == " ":
                end = True
                break
    return markers_seen, step_count, pr, pc

path = parse_input("19_input.txt")
markers, step_count, pr, pc =  follow_path(path)
print "".join(markers), step_count, (pr, pc)
