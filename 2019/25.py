import intcode

code = intcode.parse_input("25_input.txt")
vm = intcode.IntcodeVm(code)

input_string = ""
while True:
    output_data = vm.run_for_input(map(ord, input_string))
    print"".join(map(chr, output_data))
    input_string = raw_input() + "\n"
