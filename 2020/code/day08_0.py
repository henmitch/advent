"""https://adventofcode.com/2020/day/8"""
from typing import Tuple
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class Program:
    def __init__(self) -> None:
        self.accumulator: int = 0
        self.idx: int = 0
        self.seen = {0}

    def jmp(self, val: int):
        self.idx += val
        if self.looped():
            raise ValueError("Infinite loop detected")
        self.seen.add(self.idx)

    def acc(self, val: int):
        self.accumulator += val
        self.idx += 1
        if self.looped():
            raise ValueError("Infinite loop detected")
        self.seen.add(self.idx)

    def nop(self, _):
        self.idx += 1
        if self.looped():
            raise ValueError("Infinite loop detected")
        self.seen.add(self.idx)

    def looped(self):
        if self.idx in self.seen:
            return self.accumulator
        return False


def load_data(path: str) -> Tuple[Tuple[callable, int]]:
    with open(path, "r") as f:
        data = f.read().splitlines()
    out = []
    for line in data:
        line = line.split()
        out.append((line[0], int(line[1])))
    return tuple(out)


def find_first_loop(instructions: Tuple[Tuple[callable, int]]) -> int:
    p = Program()
    while True:
        instruction, val = instructions[p.idx]
        try:
            if instruction == "nop":
                p.nop(val)
            elif instruction == "acc":
                p.acc(val)
            elif instruction == "jmp":
                p.jmp(val)
        except ValueError:
            return p.accumulator


def test():
    data = load_data(TEST_PATH)
    assert find_first_loop(data) == 5


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(find_first_loop(data))
