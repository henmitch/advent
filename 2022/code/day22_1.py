"""https://adventofcode.com/2022/day/22"""
import math
from typing import Iterable

from day22_0 import DATA_PATH, TEST_PATH, Instructions, Map, extreme, load_data


class CubeMap(Map):

    def __init__(self, tiles: Iterable[complex],
                 walls: Iterable[complex]) -> None:
        super().__init__(tiles, walls)
        self.size = math.sqrt(len(self.walls) + len(self.tiles)/4)

    def wrap(self) -> complex:
        """The point we would hit if we went off the edge in the current dir"""
        if self.dir_.real:
            points = self.row(self.loc.imag)
        else:
            points = self.col(self.loc.real)

        # To combine the walls and tiles
        points = points[0]^points[1]

        return extreme(points, self.dir_)


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
    assert map_.value() == 5031


def main():
    map_, instructions = load_data(DATA_PATH)
    map_ = run_through(map_, instructions)
    print(map_.value())


if __name__ == "__main__":
    test()
    main()
