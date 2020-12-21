import intcode

code = intcode.parse_input("13.txt")

vm = intcode.IntcodeVm(code)
g = vm.run_generator()
screen = {}
for x, y, tile in zip(g, g, g):
    screen[(x, y)] = tile
print sum(1 for v in screen.values() if v == 2)


class VmManager:
    def __init__(self, vm):
        self.vm = vm
        self.vm.input_stream = self
        self.ball_x = 0
        self.paddle_x = 0
        self.score = 0


    @property
    def score(self):
        return self.screen.get((-1, 0), 0)


    def run(self):
        g = self.vm.run_generator()
        try:
            while True:
                x = next(g)
                y = next(g)
                tile = next(g)
                if (x, y) == (-1, 0):
                    self.score = tile
                elif tile == 4:
                    self.ball_x = x
                elif tile == 3:
                    self.paddle_x = x
        except StopIteration:
            return self.score


    def next(self):
        v = (self.paddle_x < self.ball_x) \
                - (self.ball_x < self.paddle_x)
        return v


code = intcode.parse_input("13.txt")
vm = intcode.IntcodeVm(code)
vm.mem[0] = 2

manager = VmManager(vm)
manager.run()
print manager.score
