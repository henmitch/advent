"""https://adventofcode.com/2023/day/9"""
import itertools

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[list[int]]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return [[int(num) for num in line.split()] for line in raw]


def sub(pair: tuple[int, int]) -> int:
    return pair[1] - pair[0]


def get_diff(nums: list[int]) -> list[int]:
    return list(map(sub, itertools.pairwise(nums)))


def predict(nums: list[int]) -> int:
    if set(nums) == {0}:
        return 0
    return nums[-1] + predict(get_diff(nums))


def run(data: list[list[int]]) -> int:
    return sum(predict(line) for line in data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 114


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
