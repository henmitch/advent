"""https://adventofcode.com/2020/day/9"""
from typing import Tuple
import day09_0 as old


def find_set(nums: Tuple[int, ...], width: int = 25) -> int:
    invalid = old.find_invalid(nums, width)
    for first in range(len(nums)):
        for last in range(first, len(nums)):
            d = nums[first:last]
            s = sum(d)
            if s > invalid:
                break
            if sum(d) == invalid:
                return min(d) + max(d)
    raise ValueError("No set found")


def test():
    data = old.load_data(old.TEST_PATH)
    assert find_set(data, 5) == 62


if __name__ == "__main__":
    test()
    data = old.load_data(old.DATA_PATH)
    print(find_set(data))
