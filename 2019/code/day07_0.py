# """https://adventofcode.com/2019/day/7"""
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
        self.inputs = list(inputs).copy()
        self.ops = {
            1: self.add,
            2: self.multiply,
            3: self.save,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
        }
        # 0 is position mode
        # 1 is immediate mode
        self.mode = 0
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
            99: 0,
        }
        # Writers should default to having their last parameter in position
        # mode, while everybody else should default to immediate mode
        self.writers = {1, 2, 7, 8}
        self.out = None
        self.verbose = verbose

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, num: int) -> int:
        # Immediate mode
        if self.mode:
            return self.data[num]
        # Position mode
        return self.data[self.data[num]]

    def __setitem__(self, idx: int, value: int) -> int:
        self.data[idx] = value

    def __repr__(self) -> str:
        return str(self.data)

    def opcode(self) -> tuple[int]:
        word = str(self.data[self.position])
        code = int(word[-2:])
        if code in self.writers:
            word = "1" + word.zfill(self.n_params[code] + 1)
        else:
            word = word.zfill(self.n_params[code] + 2)
        return tuple(int(i) for i in word[:-2]) + (code, )

    def step(self) -> None:
        opcode = self.opcode()
        try:
            func = self.ops[opcode[-1]]
        except KeyError:
            raise ValueError(f"could not find opcode {opcode[-1]}")
        func(opcode[:-1])

    def get_params(self, modes: tuple[int, ...]):
        """Return the values to be input into a given function"""
        params = []
        for i, mode in enumerate(modes[::-1]):
            self.mode = mode
            params += [self[self.position + i + 1]]
        self.position += len(modes) + 1
        return params

    def run(self) -> int:
        while self.opcode() != (99, ):
            self.step()
        return self

    # FUNCTIONS

    def add(self, modes: tuple[int, int]) -> None:
        l1, l2, lo = self.get_params(modes)
        self[lo] = l1 + l2

    def multiply(self, modes: tuple[int, int]) -> None:
        l1, l2, lo = self.get_params(modes)
        self[lo] = l1*l2

    def save(self, _) -> None:
        self[self.data[self.position + 1]] = self.inputs.pop(0)
        self.position += 2

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
        l1, l2, lo = self.get_params(modes)
        self[lo] = int(l1 < l2)

    def equals(self, modes: tuple[int, int, int]) -> None:
        l1, l2, lo = self.get_params(modes)
        self[lo] = int(l1 == l2)


###########################################################################3


def run_once(data: list[int], order: int | list = None) -> int:
    output = 0
    for num in order:
        ic = IntCode(data, (num, output))
        output = ic.run().out
    return output


def run(data: list) -> int:
    orders = itertools.permutations(range(5))
    out = 0
    for order in orders:
        out = max(out, run_once(data, order))
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 65210


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
