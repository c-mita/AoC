"""
Part 1 is solved with a regex.
Part 2 is solved by parsing JSON...

The parsing is a tad awkward because there's no peek on Python's iterators,
which means parsing a value consumes whatever symbol comes after the value
(apart from strings, which have a natural '"' marker, but we consume an
extra character just to be consistent).
"""

import re


def parse_file(filename):
    with open(filename) as f:
        return f.readlines()[0].strip()


def parse_string(stream):
    chars = []
    for c in stream:
        if c == "\"":
            next(stream) # always consume token after value...
            return "".join(chars)
        chars.append(c)


def parse_int(stream, prefix=""):
    digits = []
    for c in stream:
        if c in ":,]}":
            return int(prefix + "".join(digits))
        digits.append(c)


def parse_array(stream):
    values = list(parse_things(stream))
    return values


def parse_dict(stream):
    d = {}
    stuff = parse_things(stream)
    try:
        while True:
            key = next(stuff)
            value = next(stuff)
            d[key] = value
    except StopIteration:
        return d


def parse_things(stream):
    for symbol in stream:
        if symbol in ",]}:":
            return
        if symbol == "[":
            yield parse_array(stream)
        elif symbol == "{":
            yield parse_dict(stream)
        elif symbol == "\"":
            yield parse_string(stream)
        else:
            yield parse_int(stream, prefix=symbol)


def parse(json):
    stream = iter(json)
    return next(parse_things(stream))


def count_numbers(data):
    numbers = map(int, re.findall("-?[0-9]+", data))
    return list(numbers)


def count_numbers_no_red(json_data):
    if isinstance(json_data, str):
        return 0
    elif isinstance(json_data, int):
        return json_data
    elif isinstance(json_data, list):
        return sum(count_numbers_no_red(v) for v in json_data)
    if "red" in json_data.values():
        return 0
    keys = sum(count_numbers_no_red(k) for k in json_data)
    values = sum(count_numbers_no_red(v) for v in json_data.values())
    return keys + values



data = parse_file("12.txt")
numbers = count_numbers(data)
print(sum(numbers))

parsed_data = parse(data)
print(count_numbers_no_red(parsed_data))
