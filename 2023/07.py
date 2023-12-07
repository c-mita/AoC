"""
For part 1 we just use a comparison sort to order the hands.

For part 2, when comparing the strength of hands, we just trial every option
for the joker and take the maximum hand "rank", then perform the regular
comparison. It's a tad slow, but still <1 second.
"""

import collections
import functools


def parse_file(filename):
    data = []
    with open(filename) as f:
        for l in f:
            hand, bid = l.strip().split()
            data.append((hand, int(bid)))
    return data


def score_hand(hand):
    counter = collections.Counter(hand)
    values = tuple(sorted(counter.values()))
    if values == (5,):
        return 7
    elif values == (1, 4):
        return 6
    elif values == (2, 3):
        return 5
    elif values == (1, 1, 3):
        return 4
    elif values == (1, 2, 2):
        return 3
    elif values == (1, 1, 1, 2):
        return 2
    return 1


def hand_comparison(left, right):
    rankings = {v:n for (n, v) in enumerate("23456789TJQKA")}
    left_score, right_score = score_hand(left), score_hand(right)
    if left_score < right_score:
        return -1
    elif right_score < left_score:
        return 1
    for l, r in zip(left, right):
        rl, rr = rankings[l], rankings[r]
        if rl < rr:
            return -1
        elif rr < rl:
            return 1
    return 0


def hand_comparison_joker(left, right):
    other_cards = "23456789TQKA"
    rankings = {v:n for (n, v) in enumerate("J23456789TQKA")}
    left_score = max(score_hand(left.replace("J", j)) for j in other_cards)
    right_score = max(score_hand(right.replace("J", j)) for j in other_cards)
    if left_score < right_score:
        return -1
    elif right_score < left_score:
        return 1
    for l, r in zip(left, right):
        rl, rr = rankings[l], rankings[r]
        if rl < rr:
            return -1
        elif rr < rl:
            return 1
    return 0


test_hands = [
        ("32T3K", 765),
        ("T55J5", 684),
        ("KK677", 28),
        ("KTJJT", 220),
        ("QQQJA", 483),
]

hand_bids = test_hands
hand_bids = parse_file("07.txt")
hands = [h[0] for h in hand_bids]

ranks = sorted(hands, key=functools.cmp_to_key(hand_comparison))
hands_ranked = {hand:n+1 for n, hand in enumerate(ranks)}
print(sum(hands_ranked[hand] * bid for hand, bid in hand_bids))

joker_ranks = sorted(hands, key=functools.cmp_to_key(hand_comparison_joker))
joker_hands_ranked = {hand:n+1 for n, hand in enumerate(joker_ranks)}
print(sum(joker_hands_ranked[hand] * bid for hand, bid in hand_bids))
