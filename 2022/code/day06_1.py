"""https://adventofcode.com/2022/day/6"""
import boilerplate as bp
from day06_0 import load_data, TEST_PATH, DATA_PATH, count_leaders


def test():
    data = load_data(TEST_PATH)
    assert count_leaders(data, 14) == 19


def main():
    data = load_data(DATA_PATH)
    print(count_leaders(data, 14))


if __name__ == "__main__":
    test()
    main()
