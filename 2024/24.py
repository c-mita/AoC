"""
Part 1 is easy enough; just build up the virtual circuit and "run" it.

Part 2 is clearly this year's big "inspect the input" problem.

We are at least told it is a circuit to add things.
Shoving the circuit graph into graphviz shows us it is a simple
"Ripple-Carry-Adder" (a chain of simple Full Adders)

Inspection reveals some oddities, but we can get an idea of where
to look by adding perform the sum normally (pulling out the bits in X and Y)
and comparing the actual sum with what our circuit outputs (simple xoring
gives us an idea of which bit is going wrong).

This takes a couple of tries with different inputs to get the circuit right,
and I have left my notes and tests as is, as well as a Python program
to convert the input to a dot file for graphviz, which helped.
"""


def parse_file(filename):
    init = {}
    gates = {}
    with open(filename) as f:
        line = next(f).strip()
        while line:
            node, v = line.split(": ")
            v = bool(int((v)))
            init[node] = v
            line = next(f).strip()
        for line in f:
            n1, op, n2, _, tgt = line.strip().split()
            gates[tgt] = (op, n1, n2)
    return init, gates


def calc_op(op, n1, n2):
    if op == "XOR":
        return n1 != n2
    elif op == "AND":
        return n1 and n2
    elif op == "OR":
        return n1 or n2
    else:
        raise ValueError("Bad operation '%s'" % op)


def run_circuit(gates, init):
    current = dict(init)
    unknown = {k for k in gates if k not in current}
    while unknown:
        for k in unknown:
            op, n1, n2 = gates[k]
            if n1 in current and n2 in current:
                v = calc_op(op, current[n1], current[n2])
                break
        else:
            raise ValueError("Could not finish")
        current[k] = v
        unknown.remove(k)
    return current


def to_int(values):
    bits = [0] * (max(int(v[1:]) for v in values) + 1)
    for v in values:
        i = int(v[1:])
        bits[i] = values[v]
    r = 0
    for v in reversed(bits):
        r <<= 1
        r += v
    return r


def int_to_values(value, prefix, bits=38):
    v = value
    bit_dict = {}
    n = 0
    while n < bits:
        bit_dict["%s%02d" % (prefix, n)] = v & 1
        n += 1
        v >>= 1
    return bit_dict


init, gates = parse_file("24.txt")

values = run_circuit(gates, init)
r = to_int({k:values[k] for k in values if k[0] == "z"})
print(r)

to_swap = [
    ("z06", "jmq"),
    ("z13", "gmh"),
    ("z38", "qrh"),
    ("rqf", "cbd"),
]

fixed = dict(gates)
for l, r in to_swap:
    fixed[l], fixed[r] = fixed[r], fixed[l]

values = run_circuit(fixed, init)
r = to_int({k:values[k] for k in values if k[0] == "z"})

x = to_int({k:init[k] for k in init if k[0] == "x"})
y = to_int({k:init[k] for k in init if k[0] == "y"})
z = x + y
print(z ^ r)

x = 0b10101010101010101010101010101010101010101010
y = 0b01010101010101010101010101010101010101010101

z = x + y
init = {}
init.update(int_to_values(x, prefix="x", bits=45))
init.update(int_to_values(y, prefix="y", bits=45))
values = run_circuit(fixed, init)
r = to_int({k:values[k] for k in values if k[0] == "z"})
print(r ^ z)

x = 12312341234
y = 12321353123

z = x + y
init = {}
init.update(int_to_values(x, prefix="x", bits=45))
init.update(int_to_values(y, prefix="y", bits=45))
values = run_circuit(fixed, init)
r = to_int({k:values[k] for k in values if k[0] == "z"})
print(r ^ z)

output = []
for l, r in to_swap:
    output.append(l)
    output.append(r)
print(",".join(sorted(output)))
"""
let op_a be the name of the "op" gate producing "a".

all outputs should be XOR except the final carry

z06 comes from an AND gate
should come from a XOR between the previous carry (an OR)
and the XOR between the x06 and y06
which is XOR_jmq (so swap with jmq)

z13 comes from an OR gate and should not
should be a XOR from a XOR of x13, y13 and the carry's "OR"
should be XOR_gmh
z13 should come from XOR_fgr
fgr should come from OR_z13 (it goes to an AND for the next carry and XOR for output)

OR_bjr is the carry from x25 and y25
inputs should come from AND of those two and AND of XOR and previous OR carry
OR_bjr comes from XOR of x25 and y25, not AND
OR_bjr has XOR_bdf as an input (via cbd) - should swap with AND_rqf
these are held by targets cbd and rqf

z38 comes from AND_z38
Should be from XOR_qrh
"""

