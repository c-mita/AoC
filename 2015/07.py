def parse_input(filename):
    data = []
    with open(filename) as f:
        for line in f:
            code, target = line.strip().split(" -> ")
            codes = code.split(" ")
            if len(codes) == 1:
                data.append(("put", codes[0], target))
            elif len(codes) == 2:
                data.append(("not", codes[1], target))
            elif len(codes) == 3:
                data.append((codes[1].lower(), codes[0], codes[2], target))
            else:
                raise ValueError("Bad code '%s'" % code)
    return data


def evaluate(circuit, target):
    reduced = {}
    def _rec(target):
        if target not in circuit:
            return int(target)
        if target in reduced:
            return reduced[target]
        code = circuit[target]
        op = code[0]

        if op == "put":
            src = code[1]
            value = _rec(src)
        elif op == "not":
            src = code[1]
            value = _rec(src)
            value ^= 0xFFFF
        elif op == "or":
            op1, op2 = code[1], code[2]
            value = _rec(op1) | _rec(op2)
        elif op == "and":
            op1, op2 = code[1], code[2]
            value = _rec(op1) & _rec(op2)
        elif op == "rshift":
            op1, op2 = code[1], code[2]
            value = _rec(op1) >> _rec(op2)
            value &= 0xFFFF
        elif op == "lshift":
            op1, op2 = code[1], code[2]
            value = _rec(op1) << _rec(op2)
            value &= 0xFFFF
        else:
            raise ValueError("Bad op '%s'" % op)

        reduced[target] = value
        return value
    return _rec(target)


data = parse_input("07.txt")
circuit = {}
for instruction in data:
    target = instruction[-1]
    circuit[target] = instruction[:-1]

wire_a = evaluate(circuit, "a")
print(wire_a)

new_circuit = dict(circuit)
new_circuit["b"] = ("put", wire_a)
new_a = evaluate(new_circuit, "a")
print(new_a)
