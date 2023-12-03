import re
import functools

RED = "red"
BLUE = "blue"
GREEN = "green"

def parse_file(filename):
    games = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            game, stuff = line.split(":")
            game = int(re.search("[0-9]+", line)[0])
            games[game] = []
            for draw in stuff.split(";"):
                draw_data = {RED:0, GREEN:0, BLUE:0}
                for colour_data in draw.split(", "):
                    n, colour = colour_data.strip().split(" ")
                    draw_data[colour] = int(n)
                games[game].append(draw_data)
    return games

def is_possible(game, limit):
    game_id, draws= game
    for draw in draws:
        if draw[RED] > limit[RED]:
            return 0
        elif draw[BLUE] > limit[BLUE]:
            return 0
        elif draw[GREEN] > limit[GREEN]:
            return 0
    return game_id


def min_possible(game):
    reds = (draw[RED] for draw in game)
    greens = (draw[GREEN] for draw in game)
    blues = (draw[BLUE] for draw in game)
    return {RED:max(reds), GREEN:max(greens), BLUE:max(blues)}


data = parse_file("02.txt")
limit = {RED:12, GREEN:13, BLUE:14}
result = sum(is_possible((game, data[game]), limit) for game in data)
print(result)

result = sum(functools.reduce(
    lambda a,b: a*b, min_possible(data[game]).values()) for game in data)
print(result)
