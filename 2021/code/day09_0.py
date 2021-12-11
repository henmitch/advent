"""https://adventofcode.com/2021/day/9"""
import logging
import os
from typing import List

import boilerplate as bp

logging.basicConfig(level=logging.INFO)

DATA_PATH = os.path.join(bp.data_dir, "day09.txt")
TEST_PATH = os.path.join(bp.test_dir, "day09.txt")


def load_data(path: str) -> list:
    """Load data from file"""
    with open(path, "r") as f:
        rows = f.read().splitlines()
    return [list(map(int, list(row))) for row in rows]


def one_d_minima(lst: list) -> list:
    """Find the indices of the local minima in a list"""
    # Need to deal with the first and last elements separately
    out = []
    if lst[0] < lst[1]:
        out.append(0)
    if lst[-1] < lst[-2]:
        out.append(len(lst) - 1)
    # Now the rest
    out += [
        i + 1 for i, (x, y, z) in enumerate(zip(lst, lst[1:], lst[2:]))
        if y < x and y < z
    ]
    return out


def row_minima(data: List[List[int]]) -> List[List[int]]:
    """Find the indices of the local minima in each row"""
    out = [one_d_minima(row) for row in data]
    return out


def column_minima(data: List[List[int]]) -> List[List[int]]:
    """Find the indices of the local minima in each column"""
    out = [one_d_minima(col) for col in zip(*data)]
    return out


def local_minima(data: List[List[int]]) -> List[int]:
    """Find the indices of the local minima in each row and column"""
    out = []
    row_mins = row_minima(data)
    col_mins = column_minima(data)
    for y, r in enumerate(data):
        for x, _ in enumerate(r):
            if x in row_mins[y] and y in col_mins[x]:
                out += [[x, y]]
    return out


def local_minima_values(data: List[List[int]]) -> List[int]:
    minima = local_minima(data)
    out = []
    for x, y in minima:
        out.append(data[y][x])
    return out


def safety(data: List[List[int]]) -> int:
    """Find the sum of the data in the safe region"""
    return sum(map(lambda x: x + 1, local_minima_values(data)))


def test():
    """Test the solution"""
    data = load_data(TEST_PATH)
    assert safety(data) == 15


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(safety(data))
