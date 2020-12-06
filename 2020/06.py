def parse_input(filename):
    responses_and, responses_or = [], []
    with open(filename) as f:
        r_and, r_or = set("abcdefghijklmnopqrstuvwxyz"), set()
        for line in f:
            l = line.strip()
            if l:
                r_or.update(l)
                r_and.intersection_update(l)
            else:
                responses_and.append(r_and)
                responses_or.append(r_or)
                r_and, r_or = set("abcdefghijklmnopqrstuvwxyz"), set()
        responses_and.append(r_and)
        responses_or.append(r_or)
    return responses_or, responses_and


g_or, g_and = parse_input("06.txt")
print sum(len(g) for g in g_or)
print sum(len(g) for g in g_and)

