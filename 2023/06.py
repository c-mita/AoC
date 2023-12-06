"""
Write down the formula for the distance traveled in terms of the boat velocity
D = Distance traveled
T = Time of the race
V = Velocity of the boat

The boat moves for a duration of (T-V)

D = V * (T - V)

Note this is a quadratic equation. Set D to the target distance

V**2 - TV + D = 0

The solutions of which are the points where we will "match" the target.
Between these solutions we will exceed it. So solve.
"""


import math


TEST_INPUT_1 = ([7, 15, 30], [9, 40, 200])
INPUT_1 = ([41, 66, 72, 66], [244, 1047, 1228, 1040])

TEST_INPUT_2 = (71530, 940200)
INPUT_2 = (41667266, 244104712281040)


def solutions(time, target):
    q = math.sqrt(time * time - 4 * target)
    v1 = (time - q) / 2
    v2 = (time + q) / 2
    return v1, v2


def number_of_options(time, target):
    v1, v2 = solutions(time, target)
    b1, b2 = math.ceil(v1), math.floor(v2)
    # handle when we land precisely on int boundaries
    # we need to "beat" the target; not match it
    if b1 == v1: b1 = b1 + 1
    if b2 == v2: b2 = b2 - 1
    # + 1 because a range of a single number has length "1"
    return b2 - b1 + 1


score = 1
for time, target in zip(*INPUT_1):
    score *= number_of_options(time, target)
print(score)

options = number_of_options(*INPUT_2)
print(options)
