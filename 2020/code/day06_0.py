"""https://adventofcode.com/2020/day/6"""
from typing import Set, Tuple

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> Tuple[Set[str]]:
    with open(path, "r") as f:
        raw = f.read()
    groups = raw.split("\n\n")
    return tuple(set(group.replace("\n", "")) for group in groups)


def count(groups: Tuple[Set[str]]) -> int:
    return sum(len(group) for group in groups)


def test():
    data = load_data(TEST_PATH)
    assert count(data) == 11


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(count(data))
