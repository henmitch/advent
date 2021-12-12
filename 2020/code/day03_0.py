"""https://adventofcode.com/2020/day/3"""
import itertools
import os
from typing import List

import boilerplate as bp

DATA_PATH = os.path.join(bp.data_dir, "day03.txt")
TEST_PATH = os.path.join(bp.test_dir, "day03.txt")


def load_data(path):
    with open(path) as f:
        lines = f.read().splitlines()
    return lines


def zoom(data: List[str], x_step: int = 3, y_step: int = 1) -> List[str]:
    out = []
    x_idx = y_idx = 0
    width, height = len(data[0]), len(data)
    while y_idx < height:
        out.append(data[y_idx][x_idx])
        x_idx = (x_idx + x_step)%width
        y_idx += y_step
    return out


def count_trees(data: List[str], x_step: int = 3, y_step: int = 1) -> int:
    contacts = zoom(data, x_step, y_step)
    return sum(1 for c in contacts if c == "#")


def test():
    data = load_data(TEST_PATH)
    assert count_trees(data) == 7


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(count_trees(data))
