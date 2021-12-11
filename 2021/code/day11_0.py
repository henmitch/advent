"""https://adventofcode.com/2021/day/11"""
import itertools
import os
from typing import List, Tuple

import boilerplate as bp

Grid = List[List[int | str]]

DATA_PATH = os.path.join(bp.data_dir, "day11.txt")
TEST_PATH = os.path.join(bp.test_dir, "day11.txt")


def load_data(path):
    with open(path, "r") as f:
        input_ = f.read().splitlines()

    out = [list(map(int, list(row))) for row in input_]

    return out


def adjacent_values(x: int, y: int,
                    data: Grid) -> Tuple[Tuple[Tuple[int]], int]:
    x_max = len(data[0]) - 1
    y_max = len(data) - 1

    x_check = {x}
    y_check = {y}

    # This set notation looks like the dumbest thing.
    if x != 0:
        x_check |= {x - 1}
    if x != x_max:
        x_check |= {x + 1}
    if y != 0:
        y_check |= {y - 1}
    if y != y_max:
        y_check |= {y + 1}

    return (((x_, y_), data[y_][x_])
            for (x_, y_) in itertools.product(x_check, y_check))


def indices_iter(data: Grid) -> iter:
    for x, y in itertools.product(range(len(data[0])), range(len(data))):
        yield x, y


def any_over(data: Grid, value: int = 9) -> bool:
    for x, y in indices_iter(data):
        if data[y][x] > value:
            return True
    return False


def step(data: Grid):
    intermediate = data.copy()
    for x, y in indices_iter(data):
        intermediate[y][x] = data[y][x] + 1
    out = intermediate.copy()
    flashed = [[False for _ in range(len(data[0]))] for __ in range(len(data))]
    while any_over(out):
        # We use copies so that we don't modify the list while iterating.
        intermediate = out.copy()
        for x, y in indices_iter(data):
            if out[y][x] > 9 and not flashed[y][x]:
                intermediate[y][x] = 0
                flashed[y][x] = True
                for (x_adj, y_adj), _ in adjacent_values(x, y, data):
                    if not flashed[y_adj][x_adj]:
                        intermediate[y_adj][x_adj] += 1
        out = intermediate.copy()
    n_flashed = sum(sum(row) for row in flashed)
    return out, n_flashed


def pretty_print(data: Grid) -> str:
    return "\n".join("".join(map(str, row)) for row in data)


def count_flashes(data: Grid, steps: int = 100) -> int:
    n_flashed = 0
    for _ in range(steps):
        data, n = step(data)
        n_flashed += n
    return n_flashed


def test():
    data = load_data(TEST_PATH)
    n = count_flashes(data)
    assert n == 1656


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(count_flashes(data))
