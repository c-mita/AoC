import collections
import itertools

Literal = collections.namedtuple("Literal", ["version", "value"])
Operator = collections.namedtuple("Operator", ["version", "type", "components"])


HEX_TO_BITS = {
    "0" : [0, 0, 0, 0],
    "1" : [0, 0, 0, 1],
    "2" : [0, 0, 1, 0],
    "3" : [0, 0, 1, 1],
    "4" : [0, 1, 0, 0],
    "5" : [0, 1, 0, 1],
    "6" : [0, 1, 1, 0],
    "7" : [0, 1, 1, 1],
    "8" : [1, 0, 0, 0],
    "9" : [1, 0, 0, 1],
    "A" : [1, 0, 1, 0],
    "B" : [1, 0, 1, 1],
    "C" : [1, 1, 0, 0],
    "D" : [1, 1, 0, 1],
    "E" : [1, 1, 1, 0],
    "F" : [1, 1, 1, 1],
}


def parse_file(filename):
    with open(filename) as f:
        return f.readlines()[0].strip()


def hex_to_binary(hexes):
    bits = []
    for c in hexes:
        bits.extend(HEX_TO_BITS[c])
    return bits


def parse_packet(bit_stream):

    def three_bits(bit_stream):
        return  4 * next(bit_stream) + 2 * next(bit_stream) + next(bit_stream)

    def four_bits(bit_stream):
        return 8 * next(bit_stream) \
                + 4 * next(bit_stream) \
                + 2 * next(bit_stream) \
                + next(bit_stream)

    packet_version = three_bits(bit_stream)
    packet_type = three_bits(bit_stream)

    if packet_type == 4:
        # parse literal
        final = False
        value = 0
        while not final:
            value *= 16
            final = not bool(next(bit_stream))
            value += four_bits(bit_stream)
        return Literal(packet_version, value)
    else:
        length_bit = next(bit_stream)
        length_bits = 11 if length_bit else 15
        length = 0
        for n in range(length_bits):
            length *= 2
            length += next(bit_stream)
        if length_bit:
            # length is number of sub-packets
            sub_packets = []
            while len(sub_packets) != length:
                sub_packet = parse_packet(bit_stream)
                sub_packets.append(sub_packet)
        else:
            # length is number of bits for sub-packets
            sub_stream = itertools.islice(bit_stream, length)
            sub_packets = []
            peek = next(sub_stream, -1)
            while peek != -1:
                sub_stream = itertools.chain([peek], sub_stream)
                sub_packet = parse_packet(sub_stream)
                sub_packets.append(sub_packet)
                peek = next(sub_stream, -1)
        return Operator(packet_version, packet_type, sub_packets)


def version_sum(root):
    s = root.version
    if hasattr(root, "components"):
        s += sum(version_sum(c) for c in root.components)
    return s


def evaluate(root):
    if hasattr(root, "value"):
        return root.value
    elif not hasattr(root, "components"):
        raise ValueError("Unhandled node type: %s" % root)
    values = [evaluate(c) for c in root.components]

    if root.type == 0:
        return sum(values)
    elif root.type == 1:
        return reduce(lambda x, y: x * y, values)
    elif root.type == 2:
        return min(values)
    elif root.type == 3:
        return max(values)
    elif root.type == 5:
        return 1 if values[0] > values[1] else 0
    elif root.type == 6:
        return 1 if values[0] < values[1] else 0
    elif root.type == 7:
        return 1 if values[0] == values[1] else 0
    else:
        raise ValueError("Unknown root type %s" % root.type)


TEST_0 = "38006F45291200"
TEST_1 = "8A004A801A8002F478"
TEST_2 = "620080001611562C8802118E34"
TEST_3 = "C0015000016115A2E0802F182340"
TEST_4 = "A0016C880162017C3686B18A3D4780"

transmission_hex = parse_file("16_input.txt")

bits = hex_to_binary(transmission_hex)
component_tree = parse_packet(iter(bits))
print(version_sum(component_tree))
print(evaluate(component_tree))
