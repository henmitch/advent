"""https://adventofcode.com/2022/day/19"""
from functools import reduce
from operator import mul

from day19_0 import DATA_PATH, TEST_PATH, Blueprint, load_data, max_geodes


def run(data: list[Blueprint]) -> int:
    return reduce(mul, (max_geodes(blueprint, 32)
                        for blueprint in data[:min(len(data), 3)]))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 3472


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
