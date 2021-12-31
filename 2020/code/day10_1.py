"""https://adventofcode.com/2020/day/10"""
from functools import cache
from typing import Tuple

from day10_0 import DATA_PATH, TEST_PATH, load_data


@cache
def count_options(nums: Tuple[int, ...], num: int = 0) -> int:
    if num == max(nums):
        return 1
    out = 0
    for addend in [1, 2, 3]:
        if num + addend in nums:
            out += count_options(nums, num + addend)
    return out


def test():
    data = load_data(TEST_PATH)
    assert count_options(data) == 19208

if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(count_options(data))
