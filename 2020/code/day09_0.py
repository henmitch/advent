"""https://adventofcode.com/2020/day/9"""
from typing import Tuple
import boilerplate as bp
import itertools

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path) -> Tuple[int, ...]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return tuple(map(int, raw))


def find_invalid(nums: Tuple[int, ...], width: int = 25) -> int:
    for i, num in enumerate(nums[width:]):
        if any(a + b == num
               for a, b in itertools.combinations(nums[i:i + width], 2)):
            continue
        return num
    raise ValueError("Not found")


def test():
    data = load_data(TEST_PATH)
    assert find_invalid(data, 5) == 127


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(find_invalid(data))
