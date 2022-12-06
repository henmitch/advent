"""https://adventofcode.com/2022/day/6"""
from collections.abc import Iterator

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> str:
    with open(path, "r") as f:
        raw = f.read().strip()
    return raw


def sliding_window(s: str, size: int = 4) -> Iterator[str]:
    for i in range(len(s) - size):
        yield s[i:i + size]


def count_leaders(data: str, size: int = 4) -> int:
    for i, substring in enumerate(sliding_window(data, size)):
        if len(set(substring)) == size:
            return i + size
    raise ValueError("No unique sets of 4 consecutive characters found")


def test():
    data = load_data(TEST_PATH)
    assert count_leaders(data) == 7


def main():
    data = load_data(DATA_PATH)
    print(count_leaders(data))


if __name__ == "__main__":
    test()
    main()
