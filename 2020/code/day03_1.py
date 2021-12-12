"""https://adventofcode.com/2020/day/3"""
from typing import List, Tuple

import day03_0 as old

GIVEN_SLOPES = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]


def megazoom(data: List[str], slopes: List[Tuple[int, int]]) -> int:
    out = 1
    for slope in slopes:
        out *= old.count_trees(data, *slope)

    return out


def test():
    data = old.load_data(old.TEST_PATH)
    assert megazoom(data, GIVEN_SLOPES) == 336


if __name__ == "__main__":
    test()
    data = old.load_data(old.DATA_PATH)
    print(megazoom(data, GIVEN_SLOPES))
