"""https://adventofcode.com/2022/day/1"""
import boilerplate as bp
from day1_0 import TEST_PATH, DATA_PATH, load_data

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def sort_counts(data: tuple[tuple[int, ...], ...]) -> list[int]:
    return sorted((sum(chunk) for chunk in data), reverse=True)


def top_three_sum(data: list[int]) -> int:
    return sum(sort_counts(data)[:3])


def test():
    data = load_data(TEST_PATH)
    assert top_three_sum(data) == 45000


def main():
    data = load_data(DATA_PATH)
    print(top_three_sum(data))


if __name__ == "__main__":
    test()
    main()
