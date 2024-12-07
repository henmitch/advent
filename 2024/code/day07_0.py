"""https://adventofcode.com/2024/day/7"""
from operator import add, mul

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class Equation:

    def __init__(self, target: int, nums: list[int]):
        self.target = target
        self.nums = nums

    def __repr__(self):
        return f"Equation({self.target}, {self.nums})"

    def __len__(self):
        return len(self.nums)

    def is_valid(self) -> bool:
        if len(self) == 2:
            return self.target in (add(*self.nums), mul(*self.nums))

        last = self.nums[-1]
        remains = self.nums[:-1]

        if self.target%last:
            # If the target is not divisible by the first number,
            # multiplication won't work
            return Equation(self.target - last, remains).is_valid()

        return (Equation(self.target//last, remains).is_valid()
                or Equation(self.target - last, remains).is_valid())


def load_data(path: str) -> list[Equation]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return [parse(line) for line in raw]


def parse(line: str) -> Equation:
    target, nums = line.split(": ")
    target = int(target)
    nums = list(map(int, nums.split(" ")))
    return Equation(target, nums)


def run(data: list[Equation]) -> int:
    out = 0
    for eq in data:
        if eq.is_valid():
            out += eq.target
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 3749


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
