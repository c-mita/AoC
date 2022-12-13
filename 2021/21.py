import collections
import itertools

"""
Part 1 is uninteresting; just simulate the game.

For part 2, note that the number of unique states in the game is actually
quite limited, despite the appearence of huge numbers and high branching
factor.
So we can construct a graph of the possible game state and then walk it
backwards tracking the ways of reaching each node (accounting for the
multiplicity of die outcomes).
"""


def deterministic_die():
    while True:
        for v in range(1, 101):
            yield v

def play_game(p1_start, p2_start, die):
    s1, s2 = 0, 0
    rolls = 0
    p1, p2 = p1_start - 1, p2_start - 1
    while True:
        r1, r2, r3 = next(die), next(die), next(die)
        rolls += 3
        p1 = (p1 + r1 + r2 + r3) % 10
        s1 += p1 + 1
        if s1 >= 1000:
            return s2, rolls
        r1, r2, r3 = next(die), next(die), next(die)
        rolls += 3
        p2 = (p2 + r1 + r2 + r3) % 10
        s2 += p2 + 1
        if s2 >= 1000:
            return s1, rolls


def roll_multiplicities():
    # I could be clever and work out the combinatorics
    # but that's not why I have a computer
    mul = {}
    for r1, r2, r3 in itertools.product(range(1, 4), repeat=3):
        v = r1 + r2 + r3
        if v not in mul:
            mul[v] = 0
        mul[v] += 1
    return mul


def play_quantum_game(p1_start, p2_start):
    initial_state = (p1_start - 1, 0, p2_start - 1, 0, True)
    score_counts = roll_multiplicities()
    state_graph = {initial_state:[]}
    terminal_states = []

    def forward_dfs(state):
        p1, s1, p2, s2, p1_turn = state
        p, s = (p1, s1) if p1_turn else (p2, s2)
        for r in score_counts:
            np = (p + r) % 10
            ns = s + np + 1
            mult = score_counts[r]
            if p1_turn:
                next_state = (np, ns, p2, s2, False)
            else:
                next_state = (p1, s1, np, ns, True)
            if next_state in state_graph:
                state_graph[next_state].append((state, mult))
                continue
            state_graph[next_state] = [(state, mult)]
            if ns >= 21:
                terminal_states.append(next_state)
            else:
                forward_dfs(next_state)
        return

    forward_dfs(initial_state)
    routes = {initial_state:1}
    def reverse_dfs(state):
        if state in routes:
            return routes[state]
        options = state_graph[state]
        ways = 0
        for parent, mult in options:
            ways += mult * reverse_dfs(parent)
        routes[state] = ways
        return ways

    p1_wins = 0
    p2_wins = 0
    for terminal in terminal_states:
        pos1, score1, pos2, score2, turn = terminal
        if score1 > score2:
            p1_wins += reverse_dfs(terminal)
        else:
            p2_wins += reverse_dfs(terminal)
    return p1_wins, p2_wins


TEST_1_START = 4
TEST_2_START = 8

PLAYER_1_START = 4
PLAYER_2_START = 6
losing_score, rolls = play_game(PLAYER_1_START, PLAYER_2_START, deterministic_die())
print(losing_score * rolls)

p1_wins, p2_wins = play_quantum_game(PLAYER_1_START, PLAYER_2_START)
print(max(p1_wins, p2_wins))
