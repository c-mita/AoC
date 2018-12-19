from collections import deque

"""
Exactly the same logic as 09.py, but uses collections.deque
for improved performance over manual linked-list implementation.
"""

def play_game(n_players, max_count):
    scores = [0] * n_players
    nodes = deque([0])
    for iteration in xrange(1, max_count + 1):
        if iteration % 23 == 0:
            nodes.rotate(7)
            player = (iteration - 1) % len(scores)
            scores[player] += nodes.pop() + iteration
            nodes.rotate(-1)
        else:
            nodes.rotate(-1)
            nodes.append(iteration)
    return scores


test_params = (9, 25)
test_params = (13, 7999)
game_params = (468, 71010)

params = game_params
scores = play_game(*params)
print max(scores)

big_params = params[0], params[1] * 100
scores = play_game(*big_params)
print max(scores)
