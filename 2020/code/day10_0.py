"""https://adventofcode.com/2020/day/10"""
from collections import Counter
from typing import Tuple

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> Tuple[int, ...]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return tuple(sorted(map(int, raw)))


def count(nums: Tuple[int, ...]) -> int:
    counts = Counter([3, nums[0] - 0])
    for a, b in zip(nums, nums[1:]):
        counts.update([b - a])
    return counts[1]*counts[3]


def test():
    data = load_data(TEST_PATH)
    assert count(data) == 220


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(count(data))
