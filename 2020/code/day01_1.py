"""https://adventofcode.com/2020/day/1"""
import os
from typing import List

import boilerplate as bp

DATA_PATH = os.path.join(bp.data_dir, "day01.txt")
TEST_PATH = os.path.join(bp.test_dir, "day01.txt")


def load_data(path):
    """Load data from file"""
    with open(path, "r") as f:
        return list(map(int, f.read().splitlines()))


def find_trio_product(data: List[int]) -> int:
    for i, line in enumerate(data):
        for ii, line2 in enumerate(data[i + 1:]):
            if (remainder := 2020 - line - line2) in data[ii + i + 2:]:
                return line*line2*remainder


def test():
    test_data = load_data(TEST_PATH)
    assert find_trio_product(test_data) == 241861950


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(find_trio_product(data))
