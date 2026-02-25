"""
Not very sophisticated.
There are only four ingredients, and the number of ways to sum four
non-negative integers to 100 is somewhat limited (<200,000, even when counting
symmetric options).

So just test every way of mixing the ingredients, score them, and return the max.
Part 2 is no different, we just filter for a calorie count of 500.
"""


import re


def parse_input(filename):
    data = {}
    with open(filename) as f:
        for line in f:
            name, rest = line.strip().split(": ")
            elts = map(int, re.findall("-?[0-9]+", rest))
            data[name] = tuple(elts)
    return data


def numbers_to_target(target, parts):
    if parts < 1:
        return
    if parts == 1:
        yield (target,)
        return
    for x in range(target+1):
        for sub in numbers_to_target(target - x, parts - 1):
            yield (x,) + sub


def score_cookie(data, amounts):
    scores = [0] * 4
    for ingredient, vol in zip(data, amounts):
        scores[0] += data[ingredient][0] * vol
        scores[1] += data[ingredient][1] * vol
        scores[2] += data[ingredient][2] * vol
        scores[3] += data[ingredient][3] * vol
    score = 1
    for v in scores:
        score *= v if v > 0 else 0
    return score


def count_calories(data, amounts):
    calories = 0
    for ingredient, vol in zip(data, amounts):
        calories += data[ingredient][-1] * vol
    return calories



data = parse_input("15.txt")
scores = (score_cookie(data, amounts) for amounts in numbers_to_target(100, len(data)))
print(max(scores))

cal_500_scores = (score_cookie(data, amounts)
                    for amounts in numbers_to_target(100, len(data))
                    if count_calories(data, amounts) == 500)

print(max(cal_500_scores))
