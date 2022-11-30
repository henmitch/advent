"""https://adventofcode.com/2019/day/9"""
import boilerplate as bp
import itertools
from day02_0 import load_data

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class IntCode():

    def __init__(self,
                 data: list[int],
                 inputs: int | list = None,
                 verbose: bool = False) -> None:
        self.position = 0
        self.data = [int(datum) for datum in data]
        if inputs is not None:
            if isinstance(inputs, int):
                inputs = [inputs]
            self.inputs = list(inputs).copy()
        else:
            self.inputs = []
        self.ops = {
            1: self.add,
            2: self.multiply,
            3: self.save,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            9: self.update_base,
        }
        # 0 is position mode
        # 1 is immediate mode
        # 2 is relative mode
        self.mode = 0
        self.relative_base = 0
        # How many parameters each opcode takes
        self.n_params = {
            1: 3,
            2: 3,
            3: 1,
            4: 1,
            5: 2,
            6: 2,
            7: 3,
            8: 3,
            9: 1,
            99: 0,
        }
        self.out = None
        self.verbose = verbose
        # 1 is running
        # 0 is paused
        # -1 is halted
        self.status = 1

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, num: int) -> int:
        # Immediate mode
        if self.mode == 1:
            idx = num
        # Relative mode
        elif self.mode == 2:
            idx = self.data[num] + self.relative_base
        # Position mode
        elif not self.mode:
            if num > len(self) - 1:
                return 0
            idx = self.data[num]
        if idx > len(self) - 1:
            return 0
        return self.data[idx]

    def __setitem__(self, idx: int, value: int) -> int:
        if idx > len(self) - 1:
            self.data += (idx - len(self) + 1)*[0]
        self.data[idx] = value

    def __repr__(self) -> str:
        return str(self.data)

    def opcode(self) -> tuple[int]:
        word = str(self.data[self.position])
        code = int(word[-2:])
        word = word.zfill(self.n_params[code] + 2)
        return tuple(int(i) for i in word[:-2]) + (code, )

    def step(self) -> None:
        opcode = self.opcode()
        try:
            func = self.ops[opcode[-1]]
        except KeyError:
            raise ValueError(f"could not find opcode {opcode[-1]}")
        func(opcode[:-1])

    def get_params(self, modes: tuple[int, ...], writing: bool = False):
        """Return the values to be input into a given function"""
        params = []
        for i, mode in enumerate(modes[::-1]):
            self.mode = mode
            params += [self[self.position + i + 1]]
        # We treat values indicating output indices specially
        if writing:
            params[-1] = self.data[self.position + i + 1]
            if modes[0] == 2:
                params[-1] += self.relative_base
        self.position += self.n_params[self.opcode()[-1]] + 1
        return params

    def run(self, inputs: list | int = None) -> int:
        self.status = 1
        if inputs is not None:
            self.inputs = list(inputs)
        while self.status > 0:
            if self.opcode() == (99, ):
                self.status = -1
                break
            self.step()
        return self

    # FUNCTIONS

    def add(self, modes: tuple[int, int]) -> None:
        l1, l2, lo = self.get_params(modes, writing=True)
        self[lo] = l1 + l2

    def multiply(self, modes: tuple[int, int]) -> None:
        l1, l2, lo = self.get_params(modes, writing=True)
        self[lo] = l1*l2

    def save(self, modes: tuple[int]) -> None:
        if not self.inputs:
            self.status = 0
            return
        lo, = self.get_params(modes, writing=True)
        self[lo] = self.inputs.pop(0)

    def output(self, modes: tuple[int]) -> None:
        l1, = self.get_params(modes)
        if self.verbose:
            print(l1)
        self.out = l1

    def jump_if_true(self, modes: tuple[int, int]) -> None:
        l1, l2 = self.get_params(modes)
        if l1:
            self.position = l2

    def jump_if_false(self, modes: tuple[int, int]) -> None:
        l1, l2 = self.get_params(modes)
        if not l1:
            self.position = l2

    def less_than(self, modes: tuple[int, int, int]) -> None:
        l1, l2, lo = self.get_params(modes, writing=True)
        self[lo] = int(l1 < l2)

    def equals(self, modes: tuple[int, int, int]) -> None:
        l1, l2, lo = self.get_params(modes, writing=True)
        self[lo] = int(l1 == l2)

    def update_base(self, modes: tuple[int]) -> None:
        l1, = self.get_params(modes)
        self.relative_base += l1


###########################################################################3


def run(data: list, inputs: int | list = None) -> int:
    out = IntCode(data, inputs=inputs, verbose=True).run()
    return out


def test():
    # Quine
    data = [
        109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0,
        99
    ]
    run(data)
    print()
    # 16-digit number
    data = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    run(data)
    print()
    # Middle number
    data = [104, 1125899906842624, 99]
    run(data)
    print()


def main():
    data = load_data(DATA_PATH)
    run(data, 1)


if __name__ == "__main__":
    test()
    main()
