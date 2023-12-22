"""https://adventofcode.com/2023/day/21"""
import itertools
from collections import UserList
from functools import cache
from typing import Any, Iterator, Sequence

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class GardenMap(UserList):

    def __init__(self, data: Sequence[Sequence]) -> None:
        if not data:
            self.data = [[]]
        self.height = len(data)
        self.width = len(data[0])
        super().__init__(data)
        self._hash = hash(str(self))
        self.start = [loc for loc, char in self.all_points() if char == "S"][0]

    def __getitem__(self, loc: complex) -> str:
        x, y = int(loc.real), int(loc.imag)
        return self.data[y][x]

    def __iter__(self) -> Iterator:
        return self.data.__iter__()

    def __str__(self) -> str:
        return "\n".join(["".join(map(str, row)) for row in self])

    def __hash__(self) -> int:
        return self._hash

    def all_points(self) -> Iterator[tuple[complex, Any]]:
        for y, x in itertools.product(range(self.height), range(self.width)):
            loc = complex(x, y)
            yield loc, self[loc]

    def oob(self, loc: complex) -> bool:
        return (loc.real < 0 or loc.imag < 0 or loc.real >= self.width
                or loc.imag >= self.height)

    @cache  # pylint: disable=method-cache-max-size-none
    def cardinal_neighbors(self, loc: complex) -> set[complex]:
        return {loc + d for d in [1, 1j, -1, -1j] if not self.oob(loc + d)}

    def walk(self, distance: int = 64) -> set[complex]:
        out = set()
        to_visit = {(0, self.start)}
        while to_visit:
            d, loc = to_visit.pop()
            if d == distance:
                out.add(loc)
                continue
            for neighbor in self.cardinal_neighbors(loc):
                if self[neighbor] != "#":
                    to_visit.add((d + 1, neighbor))
        return out

    def pretty_print(self, points: set[complex] = None) -> str:
        out = ""
        for y, row in enumerate(self):
            for x, char in enumerate(row):
                if complex(x, y) in points:
                    out += "O"
                else:
                    out += char
            out += "\n"
        return out.strip()


def load_data(path: str) -> GardenMap:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return GardenMap(raw)


def run(data: GardenMap, distance: int = 64) -> int:
    endpoints = data.walk(distance)
    return len(endpoints)


def test():
    data = load_data(TEST_PATH)
    assert run(data, 6) == 16


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
