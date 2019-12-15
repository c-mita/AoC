import intcode

code = intcode.parse_input("09_input.txt")

input_arr = [1]
vm = intcode.IntcodeVm(code, iter(input_arr))
print vm.run()

input_arr = [2]
vm = intcode.IntcodeVm(code, iter(input_arr))
print vm.run()
