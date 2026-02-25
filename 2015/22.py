"""
Set up up the simulation and run Djisktra's with the accumulated mana
cost as the weight function.

Conceptually simple but following the game rules makes things a little
complicated.
"""


import collections
import heapq


Player = collections.namedtuple(
    "Player",
    field_names = ["health", "mana"],
)

Boss = collections.namedtuple(
    "Boss",
    field_names = ["health", "damage"],
)

Effects = collections.namedtuple(
    "Effects",
    field_names = ["damage_tick", "mana_tick", "armour_tick", "health_loss"],
)

State = collections.namedtuple(
    "State",
    field_names = ["player", "boss", "effects"],
)

BOSS_INPUT = Boss(51, 9)
PLAYER = Player(50, 500)

NO_EFFECTS = Effects((0, 0), (0, 0), (0, 0), 0)
HARD_MODE = Effects((0, 0), (0, 0), (0, 0), 1)


def tick_effects(state):
    player, boss, effects = state
    d, d_duration = effects.damage_tick
    m, m_duration = effects.mana_tick
    a, a_duration = effects.armour_tick
    h_loss = effects.health_loss
    d_duration -= 1
    m_duration -= 1
    a_duration -= 1
    if d_duration <= 0:
        d, d_duration = 0, 0
    if m_duration <= 0:
        m, m_duration = 0, 0
    if a_duration <= 0:
        a, a_duration = 0, 0
    effects = Effects(
        damage_tick = (d, d_duration),
        mana_tick = (m, m_duration),
        armour_tick = (a, a_duration),
        health_loss = h_loss,
    )
    return State(player=player, boss=boss, effects=effects)


def apply_effects(state):
    player, boss, effects = state
    bh, bd = boss
    ph, pm = player
    armour = 0
    if effects.damage_tick[1]:
        bh -= effects.damage_tick[0]
    if effects.mana_tick[1]:
        pm += effects.mana_tick[0]
    return State(
        player=Player(health=ph, mana=pm),
        boss=Boss(health=bh, damage=bd),
        effects=effects,
    )


def choices(state):
    player, boss, effects = state
    # try magic missile
    if player.mana >= 53:
        yield 53, State(
            player = (player.health, player.mana - 53),
            boss = (boss.health - 4, boss.damage),
            effects = effects,
        )
    # try drain
    if player.mana >= 73:
        yield 73, State(
            player = (player.health + 2, player.mana - 73),
            boss = (boss.health - 2, boss.damage),
            effects = effects,
        )
    # try shield
    if effects.armour_tick[0] == 0 and player.mana >= 113:
        new_effect = Effects(
            damage_tick = effects.damage_tick,
            mana_tick = effects.mana_tick,
            armour_tick = (7, 6),
            health_loss = effects.health_loss,
        )
        new_player = Player(health=player.health, mana=player.mana - 113)
        yield 113, State(player=new_player, boss=boss, effects=new_effect)

    # try poison
    if effects.damage_tick[0] == 0 and player.mana >= 173:
        new_effect = Effects(
            damage_tick = (3, 6),
            mana_tick = effects.mana_tick,
            armour_tick = effects.armour_tick,
            health_loss = effects.health_loss,
        )
        new_player = Player(health=player.health, mana=player.mana - 173)
        yield 173, State(player=new_player, boss=boss, effects=new_effect)

    # try mana regen
    if effects.mana_tick[0] == 0 and player.mana >= 229:
        new_effect = Effects(
            damage_tick = effects.damage_tick,
            mana_tick = (101, 5),
            armour_tick = effects.armour_tick,
            health_loss = effects.health_loss,
        )
        new_player = Player(health=player.health, mana=player.mana - 229)
        yield 229, State(player=new_player, boss=boss, effects=new_effect)


def proc_boss(state):
    armour = state.effects.armour_tick[0]
    damage = state.boss.damage
    taken = max(1, damage - armour)
    return State(
        player = Player(state.player.health - taken, state.player.mana),
        boss = state.boss,
        effects = state.effects,
    )


def explore(player, boss, initial_effects):
    initial_state = State(player=player, boss=boss, effects=initial_effects)
    states = [(0, initial_state)]
    while states:
        mana_spent, state = heapq.heappop(states)

        player = state.player
        if state.effects.health_loss:
            player = Player(health = player.health - 1, mana = player.mana)
            if player.health <= 0:
                continue
            state = State(
                player = player,
                boss = state.boss,
                effects = state.effects,
            )

        state = apply_effects(state)
        # boss might die due to damage ticks
        if state.boss.health <= 0:
            return mana_spent
        state = tick_effects(state) 

        for cost, new_state in choices(state):
            new_state = apply_effects(new_state)
            if new_state.boss.health <= 0:
                return cost + mana_spent
            new_state = tick_effects(new_state)
            if new_state.boss.health <= 0:
                return cost + mana_spent

            new_state = proc_boss(new_state)
            if new_state.player.health > 0:
                heapq.heappush(states, (mana_spent + cost, new_state))
    raise ValueError("No solution!")


cost = explore(PLAYER, BOSS_INPUT, NO_EFFECTS)
print(cost)

cost = explore(PLAYER, BOSS_INPUT, HARD_MODE)
print(cost)
