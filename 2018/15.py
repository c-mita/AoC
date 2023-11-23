from collections import namedtuple, deque
from operator import mul

ELF = "elf"
GOBLIN = "goblin"

class Unit(object):
    __slots__ = ("team", "position", "attack", "health")
    def __init__(self, team, position, attack=3, health=200):
        self.team = team
        self.position = position
        self.attack = attack
        self.health = health


class ElfDeadError(Exception):
    pass


class Arena:
    def __init__(self, lines, elf_power=3):
        self.field = {} # False for impassible wall, True otherwise
        self.units = []
        e_power = elf_power
        g_power = 3
        for (y, line) in enumerate(lines):
            for (x, v) in enumerate(line):
                self.field[(x, y)] = v != "#"
                if v == "E" or v == "G":
                    self.units.append(Unit(ELF if v == "E" else GOBLIN, (x, y), attack=e_power if v == "E" else g_power))


    def fight(self, elf_death_check=False):
        rounds = 0
        #print rounds, [(u.position, u.health) for u in self.units if u.health > 0]
        while self.round(elf_death_check):
            #print rounds, [(u.position, u.team, u.health) for u in self.units if u.health > 0]
            rounds += 1
        return rounds, sum(u.health for u in self.units if u.health > 0)


    def round(self, elf_death_check=False):
        units = sorted((u for u in self.units if u.health > 0), key=lambda u: (u.position[1], u.position[0]))
        could_move = True
        for unit in units:
            if unit.health < 0:
                continue
            could_move &= self.move(unit, elf_death_check)
        return could_move


    def move(self, unit, elf_death_check=False):
        targets = [u for u in self.units if u.health > 0 and u.team != unit.team]
        if len(targets) == 0:
            return False

        move = self.find_move(unit, targets)
        if move:
            unit.position = move

        targets_in_range = [u for u in targets if
                abs(u.position[0] - unit.position[0]) + abs(u.position[1] - unit.position[1]) == 1]
        targets_in_range = sorted(targets_in_range, key=lambda u: (u.health, u.position[1], u.position[0]))
        if targets_in_range:
            target = targets_in_range[0]
            target.health -= unit.attack
            if elf_death_check:
                if target.team == ELF and target.health < 0:
                    raise ElfDeadError()

        return True


    def find_move(self, unit, targets):
        visited = {unit.position}
        occupied = {u.position for u in self.units if u.health > 0 and u is not unit}
        def candidate_neighbours(position, field, occupied):
            px, py = position
            pos = [(px, py-1), (px-1, py), (px+1, py), (px, py+1)]
            return [p for p in pos if p not in occupied and field[p]]

        target_pos = set(p for t in targets for p in candidate_neighbours(t.position, self.field, occupied))
        if unit.position in target_pos:
            return unit.position
        reachable = []

        steps = deque([(1, p, []) for p in candidate_neighbours(unit.position, self.field, occupied)])
        while steps:
            distance, position, path = steps.popleft()
            if position in visited:
                continue
            if not self.field[position] or position in occupied:
                continue
            visited.add(position)

            if position in target_pos:
                reachable.append((position, distance, path + [position]))

            next_steps = [p for p in candidate_neighbours(position, self.field, occupied) if p not in visited]
            steps.extend((distance + 1, p, path + [position]) for p in next_steps)

        if not reachable:
            return None
        # lambda arg is (pos, distance, path) tuple
        reachable = sorted(reachable, key=lambda k: (k[1], k[0][1], k[0][0]))
        pos, distance, path = reachable[0]
        return path[0]

with open("15_input.txt") as f:
    initial_layout = f.readlines()

arena = Arena(initial_layout)
rounds, score = arena.fight()
print(rounds, score)
print(rounds * score)


elf_power = 4
elves_win = False
while not elves_win:
    arena = Arena(initial_layout, elf_power)
    try:
        rounds, score = arena.fight(elf_death_check=True)
        elves_win = True
    except ElfDeadError:
        elves_win = False
        elf_power += 1

print("Required elf power %d" % elf_power)
print(rounds, score)
print(rounds * score)
