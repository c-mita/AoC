import re


def parse_input(filename):
    results = []
    with open(filename) as f:
        for line in f:
            _card, numbers = line.split(":")
            winners, found = numbers.split("|")
            winners = list(map(int, re.findall("[0-9]+", winners)))
            found = list(map(int, re.findall("[0-9]+", found)))
            results.append((winners, found))
    return results


def count_matches(winners, draw):
    matches = set(winners) & set(draw)
    return len(matches)


def match_scores(draws):
    for winners, found in draws:
        matches = count_matches(winners, found)
        if matches:
            yield 2**(matches - 1)
        else:
            yield 0


def card_counting(draws):
    multiplicities = [1] * len(draws)
    for n, (winners, found) in enumerate(draws):
        matches = count_matches(winners, found)
        if not matches:
            continue
        to_add = multiplicities[n]
        for i in range(matches):
            multiplicities[n + i + 1] += to_add
    return multiplicities


data = parse_input("04.txt")
score = sum(match_scores(data))
print(score)

card_counts = card_counting(data)
print(sum(card_counts))
