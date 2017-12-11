import re

def parse_input(filename):
    with open(filename) as f:
        return [l.strip() for l in f][0]

def filter_stream(stream):
    filtered = ""
    idx, prev_idx = 0, 0
    l = len(stream)
    while idx < l:
        if stream[idx] == "!":
            filtered += stream[prev_idx:idx]
            idx += 2
            prev_idx = idx
            continue
        idx += 1
    filtered += stream[prev_idx:idx]
    stream = filtered

    garbage_count = [0]
    def repl_func(match):
        match_len = match.end() - match.start()
        garbage_count[0] += match_len - 2
        return ""
    return re.sub("<.*?>", repl_func, filtered), garbage_count[0]

def process_stream(stream):
    filtered, g_count = filter_stream(stream)
    depth, total_score = 0, 0
    for c in filtered:
        if c == ",": continue
        elif c == "{":
            depth += 1
            total_score += depth
        elif c == "}":
            depth -= 1
    return total_score, g_count

stream = parse_input("09_input.txt")
print process_stream(stream)
