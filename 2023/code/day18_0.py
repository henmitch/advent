"""https://adventofcode.com/2023/day/18"""
import itertools
from collections import UserList
from functools import reduce
from operator import or_
from typing import Any, Iterator, Sequence

import boilerplate as bp

Instruction = tuple[complex, int, str]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

DIRECTIONS = {"R": 1 + 0j, "L": -1 + 0j, "U": 0 - 1j, "D": 0 + 1j}


def load_data(path: str) -> list[Instruction]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return [_parse(line) for line in raw]


def _parse(line: str) -> Instruction:
    direction, amount, _ = line.split()
    return DIRECTIONS[direction], int(amount)


class Array(UserList):

    def __init__(self, data: Sequence[Sequence]) -> None:
        if not data:
            self.data = [[]]
        self.height = len(data)
        self.width = len(data[0])
        super().__init__(data)

    def __getitem__(self, loc: complex) -> str:
        x, y = int(loc.real), int(loc.imag)
        return self.data[y][x]

    def __setitem__(self, loc: complex, val: Any) -> None:
        x, y = int(loc.real), int(loc.imag)
        self.data[y][x] = val

    def __iter__(self) -> Iterator:
        return self.data.__iter__()

    def __str__(self) -> str:
        return "\n".join(["".join(map(str, row)) for row in self])

    def all_points(self) -> Iterator[tuple[complex, Any]]:
        for y, x in itertools.product(range(self.height), range(self.width)):
            loc = complex(x, y)
            yield loc, self[loc]

    def oob(self, loc: complex) -> bool:
        return (loc.real < 0 or loc.imag < 0 or loc.real >= self.width
                or loc.imag >= self.height)

    def area(self) -> int:
        return sum(int(char) for _, char in self.all_points())

    def cardinal_neighbors(self, loc: complex) -> set[complex]:
        return {loc + d for d in [1, 1j, -1, -1j] if not self.oob(loc + d)}


class Lagoon:

    def __init__(self, instructions: list[Instruction]) -> None:
        self.instructions = instructions

    def create_empty_grid(self) -> tuple[Array, complex]:
        widths = [0, 1]
        heights = [0, 1]
        loc = 0 + 0j
        for direction, amount in self.instructions:
            loc += amount*direction
            widths = [min(widths[0], loc.real), max(widths[1], loc.real)]
            heights = [min(heights[0], loc.imag), max(heights[1], loc.imag)]
        widths = [int(widths[0]), int(widths[1]) + 1]
        heights = [int(heights[0]), int(heights[1]) + 1]
        grid = Array([[0 for _ in range(*widths)] for _ in range(*heights)])
        start = complex(-widths[0], -heights[0])
        return grid, start

    def create_outline(self) -> Array:
        grid, start = self.create_empty_grid()
        loc = start
        grid[loc] = 1
        for direction, amount in self.instructions:
            for _ in range(amount):
                loc += direction
                grid[loc] = 1
        return grid

    def fill_outline(self) -> Array:
        grid, start = self.create_empty_grid()
        loc = start
        grid[loc] = 1
        inside = set()
        bounds = {loc}
        for direction, amount in self.instructions:
            for _ in range(amount):
                loc += direction
                grid[loc] = 1
                bounds.add(loc)
                inside.add(loc + (1j*direction))
        inside -= bounds

        # Flood fill
        to_check: set[complex] = reduce(or_, (grid.cardinal_neighbors(i)
                                              for i in inside))
        to_check = to_check - bounds - inside
        while to_check:
            checking = to_check.pop()
            inside.add(checking)
            to_check |= grid.cardinal_neighbors(checking) - bounds - inside

        for p in inside:
            grid[p] = 1

        return grid


def run(data: list[Instruction]) -> int:
    lagoon = Lagoon(data)
    return lagoon.fill_outline().area()


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 62


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
