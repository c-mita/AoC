import intcode


test_code = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]

code = intcode.parse_input("02_input.txt")

def replace_and_execute(code, v1, v2):
    code = list(code)
    code[1], code[2] = v1, v2
    vm = intcode.IntcodeVm(code)
    vm.run()
    return vm.mem[0]

# Part 1 - just run with values 12 and 2
print replace_and_execute(code, 12, 2)


# Part 2 - brute force search over v1 v2 in range [0-99]
import itertools
for v1, v2 in itertools.product(xrange(100), xrange(100)):
    if replace_and_execute(code, v1, v2) == 19690720:
        print 100 * v1 + v2
        break
