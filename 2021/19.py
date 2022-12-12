import collections
import itertools


"""
The strategy is to identify pair-wise connections between scanners (ones
that overlap), identify the transformations to move from one frame to the
other in each pair, and then to walk the resultant graph to map all points
into a single frame of reference.

The problem of identifying overlap is handled by considering the distances
between all pairs of points within a scanner. Distances are preserved
across our transformations, so we just need to check for collisions (the
input appears to be constructed so that all distances are unique, but for
safety, we calculate both the Manhatten (L1) and Euclidean (L2) distances.

When identifying the rotation to apply we look at possible rotations of
the "difference" vector between two input points. We then look for the
rotation that maps this to a difference vector in the target scanner's
frame of reference. We also need to remember to check the reverse of this
vector because we don't know which way they should be facing (and 90 degree
rotations cannot map you to the reverse of a vector)..

Care needs to be taken with the walk since rotations and translations do
not commute.


Part 2 is, after all this setup for Part 1, really quite easy.
Just perform the exact same graph walk as for Part 1 after the
mappings between scanners have been found, but only map the centre point
(0, 0, 0) for each scanner. Then look for the greatest distance between
any two pairs of points in this much smaller set.
"""

def parse_file(filename):
    scanners = []
    current_scanner = None
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if "scanner" in line:
                if current_scanner:
                    scanners.append(current_scanner)
                current_scanner = []
            elif line:
                current_scanner.append(tuple(map(int, line.split(","))))
    if current_scanner:
        scanners.append(current_scanner)
    return scanners


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __hash__(self):
        return hash(self.x, self.y, self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __getitem__(self, idx):
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        elif idx == 2:
            return self.z
        else:
            raise IndexError

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __repr__(self):
        return "Vector(%d, %d, %d)" % (self.x, self.y, self.z)

class Frame:
    X = 2
    Y = 3
    Z = 5
    def __init__(self, x, y, z):
        allowed = (Frame.X, -Frame.X, Frame.Y, -Frame.Y, Frame.Z, -Frame.Z)
        if x not in allowed or y not in allowed or z not in allowed:
            raise ValueError("Must use correct values for x, y, z")
        self.x = x
        self.y = y
        self.z = z

    def apply(self, vector):
        # ugly because I couldn't be arsed to write proper linear algebra code
        x, y, z = None, None, None
        if self.x == Frame.X:
            x = vector.x
        elif self.x == -Frame.X:
            x = -vector.x
        elif self.x == Frame.Y:
            x = vector.y
        elif self.x == -Frame.Y:
            x = -vector.y
        elif self.x == Frame.Z:
            x = vector.z
        elif self.x == -Frame.Z:
            x = -vector.z
        else:
            raise ValueError

        if self.y == Frame.X:
            y = vector.x
        elif self.y == -Frame.X:
            y = -vector.x
        elif self.y == Frame.Y:
            y = vector.y
        elif self.y == -Frame.Y:
            y = -vector.y
        elif self.y == Frame.Z:
            y = vector.z
        elif self.y == -Frame.Z:
            y = -vector.z
        else:
            raise ValueError

        if self.z == Frame.X:
            z = vector.x
        elif self.z == -Frame.X:
            z = -vector.x
        elif self.z == Frame.Y:
            z = vector.y
        elif self.z == -Frame.Y:
            z = -vector.y
        elif self.z == Frame.Z:
            z = vector.z
        elif self.z == -Frame.Z:
            z = -vector.z
        else:
            raise ValueError

        return Vector(x, y, z)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return "Frame(%d, %d, %d)" % (self.x, self.y, self.z)


def axis_permutations(point):
    px, py, pz = point
    # there are six directions for x
    for fx, fy, fz in ((px, py, pz), (-px, -py, pz),
            (-py, px, pz), (py, -px, pz),
            (-pz, py, px), (pz, py, -px)):
        # for each direction x faces, there are four choices to rotate
        for x, y, z in ((fx, fy, fz), (fx, fz, -fy),
                (fx, -fz, fy), (fx, -fy, -fz)):
            yield x, y, z


def get_distances(scanner):
    """
    Calculate the L1 and L2 (squared) distances between every pair.
    Returns a map of this pair of distances to the triple
    ((first, second), vector between them, reverse vector)
    """
    distances = {}
    for p1, p2 in itertools.combinations(scanner, 2):
        p1x, p1y, p1z = p1
        p2x, p2y, p2z = p2
        d_l1 = abs(p1x - p2x) + abs(p1y - p2y) + abs(p1z - p2z)
        d_l2 = (p1x - p2x)**2 + (p1y - p2y)**2 + (p1z - p2z)**2
        v = (p1x - p2x), (p1y - p2y), (p1z - p2z)
        rv = (p2x - p1x), (p2y - p1y), (p2z - p1z)
        if (d_l1, d_l2) in distances:
            raise ValueError("Distance construct not unique enough")
        distances[(d_l1, d_l2)] = (p1, p2), v, rv
    return distances


def find_transformation(first_set, second_set):
    allowed_permutations = set(Frame(*v) for v in axis_permutations(Frame(Frame.X, Frame.Y, Frame.Z)))
    for d in first_set:
        (s1, t1), v1, rv1  = first_set[d]
        (s2, t2), v2, rv2 = second_set[d]
        allowed = set()
        for rot in allowed_permutations:
            if Vector(*v1) == rot.apply(Vector(*v2)):
                reverse = False
                allowed.add(rot)
            elif Vector(*v1) == rot.apply(Vector(*rv2)):
                reverse = True
                allowed.add(rot)
        allowed_permutations &= allowed

    if not len(allowed_permutations) == 1:
        raise ValueError("Cannot solve :(")
    rotation = list(allowed_permutations)[0]
    # rotation maps the second_set to the first
    m2 = rotation.apply(Vector(*t2 if reverse else s2))
    dx, dy, dz = s1[0] - m2[0], s1[1] - m2[1], s1[2] - m2[2]
    return rotation, (dx, dy, dz)


def find_overlaps(scanners):
    overlaps = collections.defaultdict(list)
    distances = [get_distances(scanner) for scanner in scanners]
    for n, m in itertools.product(range(len(scanners)), repeat=2):
        if n == m:
            continue
        # 12 overlapping points implies 12 * 11 / 2 identical segments
        # so we need to check for 66 matching distances
        matches = [k for k in distances[n] if k in distances[m]]
        if len(matches) >= 66:
            rot, trans = find_transformation(
                    {d:distances[n][d] for d in matches}, {d:distances[m][d] for d in matches}
            )
            overlaps[n].append((m, rot, trans))
    return overlaps


def map_overlaps(scanners, overlaps):
    #points = set(scanners[0])
    points = set()
    rot = Frame(Frame.X, Frame.Y, Frame.Z)
    trans = (0, 0, 0)
    mappings = {0:[]}
    to_scan = set([0])
    scanned = set([0])
    while to_scan:
        next_scan = set()
        for n in to_scan:
            scanner = scanners[n]
            for point in scanners[n]:
                for rot, trans in reversed(mappings[n]):
                    rp = rot.apply(Vector(*point))
                    point = rp[0] + trans[0], rp[1] + trans[1], rp[2] + trans[2]
                points.add(point)
            for m, rot, trans in overlaps[n]:
                if m not in scanned:
                    mappings[m] = mappings[n] + [(rot, trans)]
                    next_scan.add(m)
                    scanned.add(m)
        to_scan = next_scan
    return points


scanners = parse_file("19_input.txt")
overlaps = find_overlaps(scanners)
points = map_overlaps(scanners, overlaps)
print(len(points))


centre_points = [[(0, 0, 0)] for scanner in scanners]
remapped_centres = map_overlaps(centre_points, overlaps)
max_d = 0
for p1, p2 in itertools.combinations(remapped_centres, 2):
    d = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])
    if d > max_d:
        max_d = d
print(max_d)
