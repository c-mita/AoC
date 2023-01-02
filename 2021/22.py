"""
Part 1 can be solved exactly the same way as Part 2 (the dumb thing doesn't scale for part 2).

We solve part 2 via an axis sweep algorithm.
For a given "z" value, identify the cuboids that intersect it.
Then sweep along y and identify those that also intersect the given y value.
Then sweep along x and identify if a point should on or off, then extend this
until the next relevant "x".

A little care is needed and it unfortunately isn't as quick as I would like, but
it completes in under 10 seconds.
"""


import collections
import itertools
import re


def parse_file(filename):
    cuboids = []
    with open(filename) as f:
        for line in f:
            on = line.startswith("on")
            lx, hx, ly, hy, lz, hz = map(int, re.findall("-*[0-9]+", line))
            cuboids.append((on, (lx, hx), (ly, hy), (lz, hz)))
    return cuboids


def apply_in_region(cuboids, blx=-50, bhx=50, bly=-50, bhy=50, blz=-50, bhz=50):
    lit = set()
    for on, (lx, hx), (ly, hy), (lz, hz) in cuboids:
        if lx > bhx or ly > bhy or lz > bhz:
            continue
        if hx < blx or hy < bly or lz < blz:
            continue
        lx = lx if lx > blx else blx
        ly = ly if ly > bly else bly
        lz = lz if lz > blz else blz
        hx = hx if hx < bhx else bhx
        hy = hy if hy < bhy else bhy
        hz = hz if hz < bhz else bhz
        for point in itertools.product(
                range(lx, hx+1), range(ly, hy+1), range(lz, hz+1)):
            if on:
                lit.add(point)
            else:
                lit.discard(point)
    return lit


def count_lit(cuboids):
    def count_sweep(relevant, index):
        if index == 0:
            # only care about the state of the "last" relevant region that intersects
            # our current sweep point
            return 1 if relevant and relevant[-1][0] else 0

        # from here "z" actually means whatever axis we're currently sweeping along
        # actually starts with x, then y, then z

        # for every "relevant" z level, we need the relevant cuboids in the order they appear in the list
        # don't care if this step is particularly efficient
        z_levels = collections.defaultdict(list)
        relevant_levels = []
        for cuboid in relevant:
            lz, hz = cuboid[-index]
            relevant_levels.append(lz)
            relevant_levels.append(hz)
            # when a region ends and we move to the next "relevant" coordinate
            # we may not know if we should multiply out backwards or not
            # (say our last value was closing an "off" region and our next represents
            # an "on" region; is this "on" actually a continuation of an old region
            # or not? So we'll always start anew after every cuboid closes off)
            # Could possibly be avoided by tracking "opening" and "closing" of regions
            # instead of just positions.
            relevant_levels.append(hz + 1)

        for z in relevant_levels:
            if z in z_levels:
                continue
            l = [c for c in relevant if c[-index][0] <= z <= c[-index][1]]
            z_levels[z] = l
        # Don't need to sort because we preserve cuboid order at all times
        #for z in z_levels:
        #    z_levels[z] = sorted(z_levels[z], key=lambda v: cuboids_idx[v])
        s = 0
        z_coords = sorted(z_levels.keys())
        for z_start, z_end in zip(z_coords[:-1], z_coords[1:]):
            d = count_sweep(z_levels[z_start], index-1)
            s += d * (z_end - z_start)
        # the last z value doesn't matter (always corresponds to the additional point added)
        return s

    return count_sweep(cuboids, 3)


cuboids = parse_file("22_input.txt")
lit_points = apply_in_region(cuboids)
print(len(lit_points))

restricted = []
for cuboid in cuboids:
    on, (lx, hx), (ly, hy), (lz, hz) = cuboid
    if -50 <= lx <= hx <= 50 and -50 <= ly <= hy <= 50 and -50 <= lz <= hz <= 50:
        restricted.append(cuboid)
n_lit = count_lit(restricted)
print(n_lit)

#test_cuboids = [(True, (-49, -5), (-3, 45), (-29, 18)), (True, (-7, -6), (-3, 45), (-29, 18))]
#test_cuboids = [(False, (-49, -5), (-3, 45), (15, 16)), (True, (-49, -5), (-3, 45), (-29, 18))]
#test_cuboids = [(True, (-49, -5), (-3, 45), (-29, 18)), (False, (-49, -5), (-3, 45), (14, 16))]
#print(len(apply_in_region(test_cuboids)))
#print(count_lit(test_cuboids))

n_lit = count_lit(cuboids)
print(n_lit)
