"""https://adventofcode.com/2021/day/9"""
import itertools
import logging
from typing import List

import boilerplate as bp
import day09_0 as old

logging.basicConfig(level=logging.INFO)

DATA_PATH = bp.get_data_path()
TEST_PATH = bp.get_test_path()


def make_mask(data: List[List[int]]) -> List[List[int]]:
    out = [[0 for _ in data[0]] for _ in data]
    for y, r in enumerate(data):
        for x, depth in enumerate(r):
            if depth == 9:
                out[y][x] = -1

    minima = old.local_minima(data)
    for basin_number, (x, y), in enumerate(minima):
        out[y][x] = basin_number + 1

    return out


def adjacent_values(x: int, y: int, mask: List[List[int]]) -> List[int]:
    x_max = len(mask[0]) - 1
    y_max = len(mask) - 1

    coordinates = set()

    # This set notation looks like the dumbest thing.
    if x != 0:
        coordinates |= set(((x - 1, y), ))
    if x != x_max:
        coordinates |= set(((x + 1, y), ))
    if y != 0:
        coordinates |= set(((x, y - 1), ))
    if y != y_max:
        coordinates |= set(((x, y + 1), ))

    return {mask[y_][x_] for (x_, y_) in coordinates}


def touching_value(x: int, y: int, mask: List[List[int]], val: int) -> bool:
    """Check if a square is touching a known value"""

    return any(adj == val for adj in adjacent_values(x, y, mask))


def all_assigned(mask: List[List[int]]) -> bool:
    return all(mask[y][x] != 0 for x, y, in indices_iter(mask))


def indices_iter(mask):
    for x, y in itertools.product(range(len(mask[0])), range(len(mask))):
        yield x, y


def iterate(mask):
    if all_assigned(mask):
        return mask
    for x, y in indices_iter(mask):
        if mask[y][x] == 0:
            mask[y][x] = max(adjacent_values(x, y, mask))
    return iterate(mask)


def basin_sizes(mask) -> List[int]:
    numbers = list(itertools.chain(*mask))
    n_basins = max(numbers)
    out = []
    for i in range(n_basins + 1):
        out += [numbers.count(i)]

    return out


def get_value(data):
    mask = iterate(make_mask(data))
    sizes = list(reversed(sorted(basin_sizes(mask))))
    out = sizes[0]*sizes[1]*sizes[2]
    return out


def test():
    data = old.load_data(TEST_PATH)
    assert get_value(data) == 1134


if __name__ == "__main__":
    test()
    data = old.load_data(DATA_PATH)
    print(get_value(data))
