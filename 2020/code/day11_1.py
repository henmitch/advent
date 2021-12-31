"""https://adventofcode.com/2020/day/11"""
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


def sightline_vals(x: int, y: int, grid: Grid) -> Set[Point]:
    x_max, y_max = len(grid[0]) - 1, len(grid) - 1
    deltas = (
        (-1, -1),  # Top left
        (0, -1),  # Top middle
        (1, -1),  # Top right
        (1, 0),  # Middle right
        (1, 1),  # Bottom right
        (0, 1),  # Bottom middle
        (-1, 1),  # Bottom left
        (-1, 0),  # Middle left
    )
    out = []
    for delta in deltas:
        scalar = 1
        while True:
            x_, y_ = x + scalar*delta[0], y + scalar*delta[1]
            if x_ < 0 or y_ < 0:
                break
            try:
                if (val := grid[y_][x_]) != ".":
                    out.append(val)
                    break
            except IndexError:
                break
            scalar += 1

    return tuple(out)


@cache
def step_point(val: str, sightline: Tuple[str, ...]) -> str:
    if val == "L" and "#" not in sightline:
        return "#"
    if val == "#" and sightline.count("#") >= 5:
        return "L"
    return val


def step_grid(grid: Grid) -> Grid:
    out = []
    for y, row in enumerate(grid):
        out_line = []
        for x, val in enumerate(row):
            adj = sightline_vals(x, y, grid)
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
    assert run(data) == 26


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(run(data))
