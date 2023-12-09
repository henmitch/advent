"""https://adventofcode.com/2023/day/9"""
import boilerplate as bp
from day09_0 import get_diff, load_data

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def predict(nums: list[int]) -> int:
    if set(nums) == {0}:
        return 0
    return nums[0] - predict(get_diff(nums))


def run(data: list[list[int]]) -> int:
    return sum(predict(line) for line in data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 2


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
