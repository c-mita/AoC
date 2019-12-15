import intcode

def id_input():
    yield 1

def rad_input():
    yield 5

code = intcode.parse_input("05_input.txt")

vm = intcode.IntcodeVm(code, id_input())
print vm.run()

vm = intcode.IntcodeVm(code, rad_input())
print vm.run()
