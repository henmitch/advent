"""https://adventofcode.com/2022/day/22"""
import re
from typing import Iterable

import boilerplate as bp

Instructions = tuple[int | str, ...]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

DIRS = {"R": 0 + 1j, "L": 0 - 1j}


def parse_instructions(instructions: str) -> Instructions:
    raw = re.findall(r"([0-9]+|[LR])", instructions)
    return tuple(int(step) if step.isnumeric() else step for step in raw)


def parse_map(map_: str) -> tuple[set[complex], set[complex]]:
    tiles, walls = [], []
    for row_num, row in enumerate(map_.splitlines()):
        for col_num, char in enumerate(row):
            if char == ".":
                tiles += [col_num + 1 + (row_num + 1)*1j]
            elif char == "#":
                walls += [col_num + 1 + (row_num + 1)*1j]
    return tiles, walls


def extreme(points: set[complex], dir_: complex) -> complex:
    if dir_.real > 0 or dir_.imag > 0:  # Need minimum
        func = min
    else:
        func = max

    if dir_.real:

        def key(x: complex):
            return x.real
    else:

        def key(x: complex):
            return x.imag

    return func(points, key=key)


class Map:

    def __init__(self, tiles: Iterable[complex],
                 walls: Iterable[complex]) -> None:
        self.tiles = set(tiles)
        self.walls = set(walls)
        self.loc = extreme(self.row(1)[0], 0 + 1j)
        self.dir_ = 1 + 0j

    def row(self, num: int) -> tuple[set[complex], set[complex]]:
        tiles = {tile for tile in self.tiles if tile.imag == num}
        walls = {wall for wall in self.walls if wall.imag == num}
        return tiles, walls

    def col(self, num: int) -> tuple[set[complex], set[complex]]:
        tiles = {tile for tile in self.tiles if tile.real == num}
        walls = {wall for wall in self.walls if wall.real == num}
        return tiles, walls

    def wrap(self) -> complex:
        """The point we would hit if we went off the edge in the current dir"""
        if self.dir_.real:
            points = self.row(self.loc.imag)
        else:
            points = self.col(self.loc.real)

        # To combine the walls and tiles
        points = points[0]^points[1]

        return extreme(points, self.dir_)

    def walk(self, steps: int) -> complex:
        if self.dir_.real:  # If we're pointing horizontally, we want the row
            avail_tile, avail_wall = self.row(self.loc.imag)
        else:  # Otherwise, we want the column
            avail_tile, avail_wall = self.col(self.loc.real)
        avail = avail_tile^avail_wall

        # At each step
        for _ in range(steps):
            print(self.loc)
            # See if we've gone off the board
            if (next_step := self.loc + self.dir_) not in avail:
                next_step = self.wrap()
            # See if we've hit a wall
            if next_step in avail_wall:
                return self.loc
            self.loc = next_step

        print(self.loc)
        return self.loc

    def turn(self, dir_: str) -> complex:
        self.dir_ *= DIRS[dir_]
        return self.dir_

    def value(self) -> int:
        dir_mapping = {1 + 0j: 0, 0 + 1j: 1, -1 + 0j: 2, 0 - 1j: 3}
        return 1000*self.loc.imag + 4*self.loc.real + dir_mapping[self.dir_]


def load_data(path: str) -> tuple[Map, Instructions]:
    with open(path, "r") as f:
        map_, instructions = f.read().split("\n\n")
    map_ = Map(*parse_map(map_))
    instructions = parse_instructions(instructions)
    return map_, instructions


def run_through(map_: Map, instructions: Instructions) -> Map:
    for instruction in instructions:
        if isinstance(instruction, int):
            map_.walk(instruction)
        else:
            map_.turn(instruction)
    return map_


def test():
    map_, instructions = load_data(TEST_PATH)
    map_ = run_through(map_, instructions)
    assert map_.value() == 6032


def main():
    map_, instructions = load_data(DATA_PATH)
    map_ = run_through(map_, instructions)
    print(map_.value())


if __name__ == "__main__":
    test()
    main()
