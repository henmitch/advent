"""https://adventofcode.com/2021/day/15"""
import os
from typing import Tuple

import boilerplate as bp

Grid = Tuple[Tuple[int, ...], ...]
Point = Tuple[int, int]

DATA_PATH = os.path.join(bp.data_dir, "day15.txt")
TEST_PATH = os.path.join(bp.test_dir, "day15.txt")


def load_data(path) -> Grid:
    with open(path, "r") as f:
        raw = f.read()
    return tuple(tuple(int(c) for c in line) for line in raw.split("\n"))


def adjacents(grid: Grid, loc: Point) -> Tuple[Tuple[Point, int], ...]:
    # Shamelessly stolen from day 9 part 2.
    x, y = loc
    x_max = len(grid[0]) - 1
    y_max = len(grid) - 1

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

    return tuple(((x_, y_), grid[y_][x_]) for (x_, y_) in coordinates)


def dist(grid: Grid, start: Point, end: Point = None) -> int:
    """The Manhattan distance from our current location to the end point"""
    x, y = start
    if end is None:
        x_max, y_max = bottom_right(grid)
    else:
        x_max, y_max = end
    return abs(x_max - x) + abs(y_max - y)


def bottom_right(grid: Grid) -> Point:
    return (len(grid[0]) - 1, len(grid) - 1)


def a_star(grid: Grid, start: Point = (0, 0), end: Point = None) -> int:
    # Going from Wikipedia knowledge here, so wish me luck.
    if end is None:
        end = bottom_right(grid)

    to_review = {start}

    so_far = {start: 0}

    remaining_est = {start: dist(grid, start, end)}

    while to_review:
        current = min(to_review, key=lambda p: so_far[p] + remaining_est[p])
        if current == end:
            return so_far[current]

        to_review.remove(current)

        for adjacent, cost in adjacents(grid, current):
            new_cost = so_far[current] + cost
            if adjacent not in so_far or new_cost < so_far[adjacent]:
                so_far[adjacent] = new_cost
                remaining_est[adjacent] = dist(grid, adjacent, end)
                to_review.add(adjacent)


def test():
    grid = load_data(TEST_PATH)
    assert isinstance(grid, tuple)
    assert a_star(grid) == 40


if __name__ == "__main__":
    test()
    grid = load_data(DATA_PATH)
    print(a_star(grid))
