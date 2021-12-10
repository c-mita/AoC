"""
Really simple; just track openning braces on a stack.
A closing brace must match the top of the stack otherwise it's an error.

Completion is just adding the corresponding brace for each brace on the stack
in reverse order.
"""


class InvalidSymbol(Exception):
    def __init__(self, symbol):
        self.symbol = symbol


def parse_file(filename):
    with open (filename) as f:
        return [l.strip() for l in f]


def _process_line(line):
    opens = "[({<"
    closes = "])}>"
    reverses = {a:b for (a,b) in zip(opens + closes, closes + opens)}
    open_braces = []
    for c in line:
        if c in opens:
            open_braces.append(c)
        elif c in closes:
            if open_braces[-1] != reverses[c]:
                raise InvalidSymbol(c)
            open_braces.pop()
    completion = "".join(reverses[c] for c in reversed(open_braces))
    return completion


def process_lines(lines):
    corrupted = []
    incomplete = []
    for line in lines:
        try:
            incomplete.append(_process_line(line))
        except InvalidSymbol as e:
            corrupted.append(e.symbol)
    return incomplete, corrupted


lines = parse_file("10_input.txt")
symbol_error_scores = {
    ")" : 3,
    "]" : 57,
    "}" : 1197,
    ">" : 25137,
}

completions, corruptions = process_lines(lines)

error_score = 0
for error in corruptions:
    error_score += symbol_error_scores[error]
print(error_score)

symbol_completion_scores = {
    ")" : 1,
    "]" : 2,
    "}" : 3,
    ">" : 4,
}

completion_scores = []
for completion in completions:
    score = 0
    for c in completion:
        score *= 5
        score += symbol_completion_scores[c]
    completion_scores.append(score)

completion_scores = sorted(completion_scores)
print(completion_scores[len(completion_scores) / 2])

