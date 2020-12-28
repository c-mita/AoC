import intcode

code = intcode.parse_input("21.txt")

"""
A == ground at 1
B == ground at 2
C == ground at 3
D == ground at 4

Our jumps are 4 long.

There must be ground at 4 to jump
If not A then must jump
if not B, or not C, then can jump if D
"""
walk_script = """
NOT B J
NOT C T
OR T J
AND D J
NOT A T
OR T J
WALK
"""

"""
Running makes our jumps 8 long, not 4
So we have to check the ground 8 tiles ahead too! (register H)
"""
run_script = """
NOT B J
NOT C T
OR T J
AND D J
AND H J
NOT A T
OR T J
RUN
"""

vm = intcode.IntcodeVm(code, (ord(c) for c in walk_script[1:]))
output = vm.run()
#print "".join(chr(c) for c in output[:-1])
print output[-1]

vm = intcode.IntcodeVm(code, (ord(c) for c in run_script[1:]))
output = vm.run()
#print "".join(chr(c) for c in output[:-1])
print output[-1]
