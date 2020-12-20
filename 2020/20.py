import collections
import itertools



image_block = collections.namedtuple(
        "image_block",
        ["id", "top", "left", "bottom", "right", "transform_id", "raw"])


def parse_block_data(data):
    data = data.split("\n")
    top = tuple(1 if data[0][n] == "#" else 0 for n in range(len(data[0])))
    bottom = tuple(1 if data[-1][n] == "#" else 0 for n in range(len(data[-1])))
    left = tuple(1 if data[n][0] == "#" else 0 for n in range(len(data)))
    right = tuple(1 if data[n][-1] == "#" else 0 for n in range(len(data)))
    image = [row[1:-1] for row in data[1:-1]]
    return (top, right, bottom, left), image


def parse_file(filename):
    blocks = []
    with open(filename) as f:
        for block in f.read().strip().split("\n\n"):
            hdr, data = block.split(":\n")
            block_id = int(hdr.split(" ")[1])
            blocks.append((block_id, parse_block_data(data)))
    return blocks


def get_image_block_structs(raw_blocks):
    blocks = {}
    for block_id, (bounds, data) in raw_blocks:
        blocks[block_id] = []
        for (n, options) in enumerate(get_alternates(bounds)):
            block = image_block(
                    block_id,
                    top = options[0],
                    right = options[1],
                    bottom = options[2],
                    left = options[3],
                    transform_id = n,
                    raw = data)
            blocks[block_id].append(block)
    return blocks


def rotate(edges, length=10):
    top, right, bottom, left = edges
    new_top = tuple(reversed(left))
    new_bottom = tuple(reversed(right))
    new_right = top
    new_left = bottom
    return new_top, new_right, new_bottom, new_left


def get_flips(edges):
    top, right, bottom, left = edges
    vert = tuple(reversed(top)), left, tuple(reversed(bottom)), right
    hztl = bottom, tuple(reversed(right)), top, tuple(reversed(left))
    d1 = tuple(reversed(right)), tuple(reversed(top)), \
            tuple(reversed(left)), tuple(reversed(bottom))
    d2 = left, bottom, right, top
    return [vert, hztl, d1, d2]


def get_alternates(edges):
    r1 = edges
    r2 = rotate(r1)
    r3 = rotate(r2)
    r4 = rotate(r3)
    return [r1, r2, r3, r4] + get_flips(edges)


def fits_constraints(block, constraints):
    top, right, bottom, left = constraints
    if top and top != block.top:
        return False
    if right and right != block.right:
        return False
    if bottom and bottom != block.bottom:
        return False
    if left and left != block.left:
        return False
    return True


def get_constraints(key, placed):
    x, y = key
    left = placed[(x-1, y)].right if (x-1, y) in placed else None
    right = placed[(x+1, y)].left if (x+1, y) in placed else None
    top = placed[(x, y-1)].bottom if (x, y-1) in placed else None
    bottom = placed[(x, y+1)].top if (x, y+1) in placed else None
    return top, right, bottom, left


def get_index_bounds(placed):
    # we know (0, 0) is always a location
    minx, miny = 0, 0
    maxx, maxy = 0, 0
    for (x, y) in placed:
        minx = x if x < minx else minx
        miny = y if y < miny else miny
        maxx = x if x > maxx else maxx
        maxy = y if y > maxy else maxy
    return (minx, miny), (maxx, maxy)


def solve(blocks):
    """Just place the first block and call the recursive solution"""
    for block_id, block_set in blocks.items():
        block = block_set[0]
        break
    placed = {(0, 0) : block}
    front = {(-1, 0), (1, 0), (0, -1), (0, 1)}
    blocks = dict(blocks)
    del blocks[block_id]
    return recurse(blocks, placed, front)


def recurse(blocks, placed, front):
    if not blocks:
        return placed
    candidates = {}
    for p in front:
        candidates[p] = []
        constraints = get_constraints(p, placed)
        for ib in itertools.chain.from_iterable(iter(b for b in blocks.values())):
            if fits_constraints(ib, constraints):
                candidates[p].append(ib)
    candidates = {k:v for (k, v) in candidates.iteritems() if len(v)}
    if not candidates:
        return False

    # pick the cell with the fewest candidates
    coord = min(candidates, key=lambda v: len(candidates[v]))
    cx, cy = coord
    for block in candidates[coord]:
        new_blocks = dict(blocks)
        del new_blocks[block.id]
        new_placed = dict(placed)
        new_placed[coord] = block
        new_front = front - {coord}
        neighbours = [(cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1)]
        new_front |= {v for v in neighbours if v not in placed}
        v = recurse(new_blocks, new_placed, new_front)
        if v:
            return v


def rotate_data(data):
    rdata = []
    for r in data:
        rdata.append([])
    for row in reversed(data):
        for n, v in enumerate(row):
            rdata[n].append(v)
    return rdata


def flip_data_h(data):
    return list(reversed(data))


def flip_data_v(data):
    return [list(reversed(row)) for row in data]


def flip_data_d1(data):
    rdata = []
    s = len(data)
    for n in reversed(range(s)):
        rdata.append([row[n] for row in reversed(data)])
    return rdata


def flip_data_d2(data):
    rdata = []
    s = len(data)
    for n in range(s):
        rdata.append([row[n] for row in data])
    return rdata


def transform_data(data, transform_key=0):
    if 0 <= transform_key < 4:
        rdata = data
        for n in range(transform_key):
            rdata = rotate_data(rdata)
        return rdata
    elif transform_key == 4:
        return flip_data_v(data)
    elif transform_key == 5:
        return flip_data_h(data)
    elif transform_key == 6:
        return flip_data_d1(data)
    elif transform_key == 7:
        return flip_data_d2(data)
    else:
        raise ValueError("Bad key")


def generate_image(blocks):
    (minx, miny), (maxx, maxy) = get_index_bounds(blocks)
    sx = len(blocks.values()[0].raw[0])
    sy = len(blocks.values()[0].raw)
    image = {}
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            block = blocks[(x, y)]
            data = transform_data(block.raw, block.transform_id)
            for ny, brow in enumerate(data):
                dy = ny + (sy * y)
                dy -= sy * miny
                for nx, c in enumerate(brow):
                    dx = nx + (sx * x)
                    dx -= sx * minx
                    image[(dx, dy)] = c

    (_, _), (maxx, maxy) = get_index_bounds(image)
    image_data = []
    for y in range(maxy+1):
        image_data.append([image[(x, y)] for x in range(maxx+1)])
    return image_data


def match_pattern(pattern, data):
    for p, v in zip(pattern, data):
        if p == "#" and v != p:
            return False
    return True


def count_waves(image):
    pattern = [
            "                  # ",
            "#    ##    ##    ###",
            " #  #  #  #  #  #   "]
    monster_cell_count = sum(sum(1 for v in row if v == "#") for row in pattern)
    wave_count = sum(sum(1 for v in row if v == "#") for row in image)
    lpattern = len(pattern[1])
    sy, sx = len(image), len(image[0])
    for tk in range(8):
        data = transform_data(image, tk)
        monster_count = 0
        for n in range(1, sy-1):
            for m in range(sx - lpattern):
                if match_pattern(pattern[1], data[n][m:m+lpattern]) \
                        and match_pattern(pattern[2], data[n+1][m:m+lpattern]) \
                        and match_pattern(pattern[0], data[n-1][m:m+lpattern]):
                    monster_count += 1
        if monster_count > 0:
            return wave_count - monster_count * monster_cell_count


raw_blocks = parse_file("20.txt")
blocks = get_image_block_structs(raw_blocks)
mapped_blocks = solve(blocks)
(minx, miny), (maxx, maxy) = get_index_bounds(mapped_blocks)
v1 = mapped_blocks[(minx, miny)].id
v2 = mapped_blocks[(minx, maxy)].id
v3 = mapped_blocks[(maxx, miny)].id
v4 = mapped_blocks[(maxx, maxy)].id
print v1 * v2 * v3 * v4

image = generate_image(mapped_blocks)
image = transform_data(image, 5)
print count_waves(image)
