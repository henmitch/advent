"""https://adventofcode.com/2020/day/5"""
from typing import Tuple

import day05_0 as old


def find_missing(seats: Tuple[old.Seat]) -> int:
    seats = set(map(old.value, seats))
    for seat in range(min(seats), max(seats) + 1):
        if {seat - 1, seat + 1} <= seats and seat not in seats:
            return seat
    raise ValueError("Missing!")


if __name__ == "__main__":
    data = old.load_data(old.DATA_PATH)
    print(find_missing(data))
