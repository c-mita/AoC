import re


def parse_expression(expr):
    return re.findall("\(|\)|\d+|\+|\*", expr)


def parse_file(filename):
    with open(filename) as f:
        return [parse_expression(l.strip()) for l in f]


def product(values):
    return reduce(lambda v1,v2: v1*v2, values)


def eval_l2r(expr_stream):
    r, op = None, None
    for s in expr_stream:
        if s == ")":
            return r
        elif s == "+" or s == "*":
            op = s
        elif s == "(":
            v = eval_l2r(expr_stream)
            if op == "*": r *= v
            elif op == "+": r += v
            else: r = v
        else:
            if not op: r = int(s)
            elif op == "*": r *= int(s)
            elif op == "+": r += int(s)
    return r


def eval_expr(expr_stream):
    values = []
    for s in expr_stream:
        if s == ")":
            break
        elif s == "(":
            v = eval_expr(expr_stream)
            values.append(v)
        elif s == "+":
            v = eval_expr(expr_stream)
            values[-1] += v
        elif s == "*":
            values.append(eval_expr(expr_stream))
        else:
            return int(s)
    return product(values)


def evaluate_simple(expression):
    return eval_l2r(iter(expression))


def evaluate_algebraic(expression):
    # we depend on the closing bracket to back out of the recursion at
    # the correct time. This is a "wee bit" hacky...
    expression = ["("] + expression + [")"]
    return eval_expr(iter(expression))


expressions = parse_file("18.txt")
print sum(evaluate_simple(e) for e in expressions)
print sum(evaluate_algebraic(e) for e in expressions)
