"""https://adventofcode.com/2024/day/7"""
from operator import add, mul

import boilerplate as bp
from day07_0 import DATA_PATH, TEST_PATH, Equation


class Equation2(Equation):

    def __repr__(self):
        return f"Equation2({self.target}, {self.nums})"

    def is_valid(self) -> bool:
        if len(self) == 2:
            return self.target in (add(*self.nums), mul(*self.nums),
                                   concat(*self.nums))

        last = self.nums[-1]
        remains = self.nums[:-1]

        to_check: list[Equation2] = []

        if not self.target%last:
            # If the target is divisible by the last number, multiplication
            # could work
            to_check.append(Equation2(self.target//last, remains))

        if self.target - last >= 0:
            # If the target is greater than the last number, addition could
            # work
            to_check.append(Equation2(self.target - last, remains))

        if is_deconcatable(self.target, last):
            # If the target is deconcatable by the last number, concatenation
            # could work
            to_check.append(Equation2(deconcat(self.target, last), remains))

        return any(eq.is_valid() for eq in to_check)


def load_data(path: str) -> list[Equation2]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return [parse(line) for line in raw]


def parse(line: str) -> Equation2:
    target, nums = line.split(": ")
    target = int(target)
    nums = list(map(int, nums.split(" ")))
    return Equation2(target, nums)


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def deconcat(big: int, small: int) -> int:
    if not is_deconcatable(big, small):
        raise ValueError(f"{big} is not deconcatable by {small}")
    return int(str(big)[:-len(str(small))])


def is_deconcatable(big: int, small: int) -> bool:
    return str(small) == str(big)[-len(str(small)):]


def run(data: list[Equation2]) -> int:
    out = 0
    for eq in data:
        if eq.is_valid():
            out += eq.target
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 11387


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
