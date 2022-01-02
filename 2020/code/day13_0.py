"""https://adventofcode.com/2020/day/13"""
from typing import Tuple
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> Tuple[int, Tuple[int, ...]]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    target = int(raw[0])
    periods = tuple(int(x) for x in raw[1].split(",") if x != "x")
    return target, periods


def next_time(target: int, period: int) -> int:
    return target + period - target%period


def find_next(target: int, periods: Tuple[int, ...]) -> Tuple[int, int]:
    return min(((next_time(target, period), period) for period in periods),
               key=lambda x: x[0])


def run(data: Tuple[int, Tuple[int, ...]]) -> int:
    found = find_next(*data)
    return (found[0] - data[0])*found[1]


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 295


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(run(data))
