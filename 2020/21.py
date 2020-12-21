import collections
import itertools



def parse_file(filename):
    allergen_map = collections.defaultdict(list)
    recipes = []
    with open(filename) as f:
        for line in f:
            b1, b2 = line.strip().split(" (contains ")
            ingredients = set(b1.split(" "))
            allergens = b2.strip(")").split(", ")
            for a in allergens:
                allergen_map[a].append(ingredients)
            recipes.append(ingredients)
    return allergen_map, recipes


def get_ingredients(allergen_map):
        return reduce(
            lambda s1,s2: s1 | s2,
            itertools.chain(s for v in allergen_map.values() for s in v),
            set())


def reduce_allergens(allergen_map):
    reduced_map = {}
    for a in allergen_map:
        candidates = reduce(lambda s1,s2: s1 & s2, allergen_map[a])
        reduced_map[a] = candidates
    return reduced_map


def find_safe_ingredients(allergen_map):
    ingredients = get_ingredients(allergen_map)
    allergen_map = reduce_allergens(allergen_map)
    known = {}
    while True:
        next_map = {}
        allergen, ingredient = None, None
        for (a, s) in allergen_map.items():
            if len(s) == 1:
                ingredient = next(iter(s))
                allergen = a
                known[a] = ingredient
                break
        else:
            return known, ingredients - set(known.values())
        for a in (a for a in allergen_map if a != allergen):
            s = allergen_map[a] - {ingredient}
            if len(s) == 0:
                raise ValueError("Inconsistency found")
            next_map[a] = s
        allergen_map = next_map


allergen_map, recipes = parse_file("21.txt")
allergens, safe = find_safe_ingredients(allergen_map)
print sum(sum(1 for v in r if v in safe) for r in recipes)
print ",".join(allergens[v] for v in sorted(allergens))
