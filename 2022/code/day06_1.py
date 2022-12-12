"""https://adventofcode.com/2022/day/6"""
from day06_0 import DATA_PATH, TEST_PATH, count_leaders, load_data


def test():
    data = load_data(TEST_PATH)
    assert count_leaders(data, 14) == 19


def main():
    data = load_data(DATA_PATH)
    print(count_leaders(data, 14))


if __name__ == "__main__":
    test()
    main()
