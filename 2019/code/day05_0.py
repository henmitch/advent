"""https://adventofcode.com/2019/day/5"""
import boilerplate as bp
from day02_0 import load_data

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class IntCode():

    def __init__(self, data: list[int], input_: int = None) -> None:
        self.position = 0
        self.data = [int(datum) for datum in data]
        self.input_ = input_
        self.ops = {
            1: self.add,
            2: self.multiply,
            3: self.save,
            4: self.output,
        }
        # 0 is position mode
        # 1 is immediate mode
        self.mode = 0
        self.n_params = {1: 3, 2: 3, 3: 1, 4: 1, 99: 0}

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
        word = word.zfill(self.n_params[code] + 1)
        # In case we need to add a "1" for the saving position
        word = word.rjust(self.n_params[code] + 2, "1")
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
        return self[0]

    # FUNCTIONS

    def add(self, modes: tuple[int, int]) -> None:
        l1, l2, lo = self.get_params(modes)
        self[lo] = l1 + l2

    def multiply(self, modes: tuple[int, int]) -> None:
        l1, l2, lo = self.get_params(modes)
        self[lo] = l1*l2

    def save(self, _) -> None:
        self[self.data[self.position + 1]] = self.input_
        self.position += 2

    def output(self, modes: tuple[int]) -> int:
        l1, = self.get_params(modes)
        print(self[l1])


###########################################################################3


def run(data: list[int], input_: int = None) -> int:
    ic = IntCode(data, input_)
    return ic.run()


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 3500
    ic1 = IntCode([1002, 4, 3, 4, 33])
    ic1.run()
    assert ic1.data == [1002, 4, 3, 4, 99]
    ic2 = IntCode([1101, 100, -1, 4, 0])
    ic2.run()
    assert ic2.data == [1101, 100, -1, 4, 99]


def main():
    data = load_data(DATA_PATH)
    run(data, 1)


if __name__ == "__main__":
    test()
    main()
