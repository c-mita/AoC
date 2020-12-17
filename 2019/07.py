import itertools
import intcode


code = intcode.parse_input("07.txt")

max_v = (0, None)
for p in itertools.permutations([0, 1, 2, 3, 4]):
    a1 = intcode.IntcodeVm(code, iter([p[0], 0]))
    a2 = intcode.IntcodeVm(code, itertools.chain([p[1]], a1.run_generator()))
    a3 = intcode.IntcodeVm(code, itertools.chain([p[2]], a2.run_generator()))
    a4 = intcode.IntcodeVm(code, itertools.chain([p[3]], a3.run_generator()))
    a5 = intcode.IntcodeVm(code, itertools.chain([p[4]], a4.run_generator()))
    v = next(a5.run_generator())
    max_v = (v, p) if v > max_v[0] else max_v
print max_v


max_v = (0, None)
for p in itertools.permutations([5, 6, 7, 8, 9]):
    a1, a2, a3, a4, a5 = (intcode.IntcodeVm(code) for n in range(5))
    a1.input_stream = iter([p[0], 0])
    a2.input_stream = iter([p[1]])
    a3.input_stream = iter([p[2]])
    a4.input_stream = iter([p[3]])
    a5.input_stream = iter([p[4]])
    g1, g2, g3, g4, g5 = (a.run_generator() for a in (a1, a2, a3, a4, a5))
    v = 0
    try:
        while True:
            a2.input_stream = itertools.chain(a2.input_stream, iter([next(g1)]))
            a3.input_stream = itertools.chain(a3.input_stream, iter([next(g2)]))
            a4.input_stream = itertools.chain(a4.input_stream, iter([next(g3)]))
            a5.input_stream = itertools.chain(a5.input_stream, iter([next(g4)]))
            v = next(g5)
            a1.input_stream = itertools.chain(a1.input_stream, iter([v]))
    except StopIteration:
        pass
    max_v = (v, p) if v > max_v[0] else max_v
print max_v

