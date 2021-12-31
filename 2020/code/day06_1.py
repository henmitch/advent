"""https://adventofcode.com/2020/day/6"""
from typing import Tuple

import day06_0 as old


def load_data(path: str) -> Tuple[Tuple[str]]:
    with open(path, "r") as f:
        raw = f.read()
    groups = raw.split("\n\n")
    return tuple(tuple(group.splitlines()) for group in groups)


def count(groups: Tuple[Tuple[str]]) -> int:
    return sum(
        sum("".join(group).count(i) == len(group) for i in set("".join(group)))
        for group in groups)


def test() -> int:
    data = load_data(old.TEST_PATH)
    assert count(data) == 6


if __name__ == "__main__":
    test()
    data = load_data(old.DATA_PATH)
    print(count(data))
