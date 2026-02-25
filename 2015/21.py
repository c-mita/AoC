"""
Simulation of the game is a simple calculation.

Part 1 - we just test every combination of permitted purchased items.

Part 2 - test every item in the power set of "armour + rings".
 - the problem text isn't clear, but we are still constrained
   to purchasing exactly one weapon.

A pro would use itertools.
"""


import math


BOSS_INPUT = (100, 8, 2)
PLAYER = (100, 0, 0)

WEAPONS = [
    (8, 4, 0),
    (10, 5, 0),
    (25, 6, 0),
    (40, 7, 0),
    (74, 8, 0),
]

ARMOUR = [
    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5),
]

RINGS = [
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3),
]

NOTHING = (0, 0, 0)


def weapon_choices(weapons):
    for weapon in weapons:
        yield weapon


def armour_choices(armours):
    yield NOTHING
    for armour in armours:
        yield armour


def ring_choices(rings):
    rings = rings + [NOTHING]
    yield (NOTHING, NOTHING)
    for i in range(len(rings)):
        for j in range(i+1, len(rings)):
            yield (rings[i], rings[j])


def powerset(items):
    def _powerset(idx):
        if idx >= len(items):
            yield ()
            return
        item = (items[idx],)
        for partial in _powerset(idx+1):
            yield partial
            yield partial + item
    return _powerset(0)


def player_wins(player, boss):
    ph, pd, pa = player
    bh, bd, ba = boss
    p_hit = max(1, pd - ba)
    b_hit = max(1, bd - pa)
    p_kill = math.ceil(bh / p_hit)
    b_kill = math.ceil(ph / b_hit)
    return p_kill <= b_kill

        
p_health, p_dmg, p_armour = PLAYER
lowest_cost = 0x7FFFFFFF
for weapon in weapon_choices(WEAPONS):
    w_cost, w_dmg, w_armour = weapon
    for armour in armour_choices(ARMOUR):
        a_cost, a_dmg, a_armour = armour
        for ring1, ring2 in ring_choices(RINGS):
            r1_cost, r1_dmg, r1_armour = ring1
            r2_cost, r2_dmg, r2_armour = ring2
            cost = w_cost + a_cost + r1_cost + r2_cost
            dmg = p_dmg + w_dmg + a_dmg + r1_dmg + r2_dmg
            armour = p_armour + w_armour + a_armour + r1_armour + r2_armour
            if player_wins((p_health, dmg, armour), BOSS_INPUT):
                lowest_cost = min(lowest_cost, cost)
print(lowest_cost)

highest_cost = 0
for weapon in weapon_choices(WEAPONS):
    w_cost, w_dmg, w_armour = weapon
    for combination in powerset(ARMOUR + RINGS):
        cost = w_cost + sum(item[0] for item in combination)
        dmg = w_dmg + sum(item[1] for item in combination)
        armour = w_armour + sum(item[2] for item in combination)
        if not player_wins((p_health, dmg, armour), BOSS_INPUT):
            highest_cost = max(highest_cost, cost)
print(highest_cost)
