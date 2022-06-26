"""https://adventofcode.com/2019/day/2"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[int]:
    with open(path, "r") as f:
        raw = f.read()
    return [int(num) for num in raw.split(",")]


class IntCode:

    def __init__(self,
                 data: list[int],
                 noun: int = None,
                 verb: int = None) -> None:
        self.position = 0
        self.data = [int(datum) for datum in data]
        if noun is not None:
            self.data[1] = noun
        if verb is not None:
            self.data[2] = verb
        self.ops = {1: self.add, 2: self.multiply}

    def __getitem__(self, idx: int) -> int:
        return self.data[idx]

    def __setitem__(self, idx: int, value: int) -> int:
        self.data[idx] = value

    def __repr__(self) -> str:
        return str(self.data)

    def opcode(self) -> int:
        return self.data[self.position]

    def step(self) -> None:
        opcode = self.opcode()
        try:
            func = self.ops[opcode]
        except KeyError:
            raise ValueError(f"could not find opcode {opcode}")
        func()

    def run(self) -> int:
        while self.opcode() != 99:
            self.step()
        return self[0]

    def add(self) -> None:
        l1, l2, lo = self[self.position + 1:self.position + 4]
        self[lo] = self[l1] + self[l2]
        self.position += 4

    def multiply(self) -> None:
        l1, l2, lo = self[self.position + 1:self.position + 4]
        self[lo] = self[l1]*self[l2]
        self.position += 4


def run(data: list[int], noun: int = None, verb: int = None) -> int:
    ic = IntCode(data, noun, verb)
    return ic.run()


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 3500


def main():
    data = load_data(DATA_PATH)
    print(run(data, 12, 2))


if __name__ == "__main__":
    test()
    main()
