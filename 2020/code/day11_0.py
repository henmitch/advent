"""https://adventofcode.com/2020/day/11"""
import itertools
from functools import cache
from typing import List, Set, Tuple

import boilerplate as bp

Grid = List[List[str]]
Point = Tuple[int, int]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> Grid:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return [list(line) for line in raw]


@cache
def adjacent_coords(x: int, y: int, x_max: int, y_max: int) -> Set[Point]:
    xs = {x}
    ys = {y}
    if x > 0:
        xs |= {x - 1}
    if x < x_max - 1:
        xs |= {x + 1}
    if y > 0:
        ys |= {y - 1}
    if y < y_max - 1:
        ys |= {y + 1}
    return set(itertools.product(xs, ys)) - {(x, y)}


def adjacent_vals(x: int, y: int, grid: Grid) -> Tuple[str]:
    x_max, y_max = len(grid[0]), len(grid)
    return tuple(grid[y_][x_]
                 for x_, y_ in adjacent_coords(x, y, x_max, y_max))


@cache
def step_point(val: str, adj: Tuple[str, ...]) -> str:
    if val == "L" and "#" not in adj:
        return "#"
    if val == "#" and adj.count("#") >= 4:
        return "L"
    return val


def step_grid(grid: Grid) -> Grid:
    out = []
    for y, row in enumerate(grid):
        out_line = []
        for x, val in enumerate(row):
            adj = adjacent_vals(x, y, grid)
            out_line.append(step_point(val, adj))
        out.append(out_line)
    return out


def run_until_done(grid: Grid) -> Grid:
    stepped = step_grid(grid)
    while stepped != grid:
        grid = stepped
        stepped = step_grid(grid)

    return stepped


def count_full(grid: Grid) -> int:
    return sum(sum(val == "#" for val in row) for row in grid)


def run(grid: Grid) -> int:
    stepped = run_until_done(grid)
    return count_full(stepped)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 37


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(run(data))
