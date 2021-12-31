"""https://adventofcode.com/2020/day/5"""
import re
from typing import Tuple

import boilerplate as bp

Seat = Tuple[str, str]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> Tuple[Seat]:
    with open(path, "r") as f:
        raw = f.read()
    raw = re.sub("[FL]", "0", raw)
    replaced = re.sub("[BR]", "1", raw)
    data = replaced.splitlines()
    out = []
    for line in data:
        out.append((line[:7], line[7:]))
    return tuple(out)


def value(seat: Seat) -> int:
    return 8*int(seat[0], 2) + int(seat[1], 2)


def highest(seats: Tuple[Seat]) -> int:
    return max(value(seat) for seat in seats)


if __name__ == "__main__":
    data = load_data(DATA_PATH)
    print(highest(data))
