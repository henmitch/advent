"""https://adventofcode.com/2023/day/14"""
import itertools
from collections import UserList
from typing import Any, Iterable, Iterator, Sequence

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


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

    def all_points(self) -> Iterator[tuple[complex, str]]:
        for y, x in itertools.product(range(self.height), range(self.width)):
            loc = complex(x, y)
            yield loc, self[loc]

    def __iter__(self) -> Iterator:
        return self.data.__iter__()


class Platform:

    def __init__(self, drawing: str) -> None:
        self.map = Array(drawing.splitlines())
        self.width = self.map.width
        self.height = self.map.height

    def __getitem__(self, loc: complex) -> str:
        return self.map[loc]

    def all_points(self) -> Iterable[tuple[complex, str]]:
        yield from self.map.all_points()

    def get_locations(self) -> dict[str, set[complex]]:
        out = {}
        for loc, char in self.all_points():
            # Ignore spaces with no rocks
            if char == ".":
                continue
            out[char] = out.get(char, set()) | {loc}
        return out

    def find_spaces_north(self) -> Array:
        spaces_north = Array([[0 for _ in range(self.width)]
                              for _ in range(self.height)])
        tracking = [0 for _ in range(self.width)]
        for y in range(1, self.height):
            for x in range(self.width):
                loc = complex(x, y)
                above = self[loc - 1j]
                if above == ".":
                    tracking[x] += 1
                elif above == "#":
                    tracking[x] = 0
                elif above == "O":
                    pass
                else:
                    raise ValueError(f"Found bad character {above} at {loc}")
                spaces_north[loc] = tracking[x]
        return spaces_north

    def get_load(self) -> int:
        spaces_north = self.find_spaces_north()
        out = 0
        for loc, char in self.all_points():
            y = int(loc.imag)
            if char == "O":
                out += self.height - (y - spaces_north[loc])
        return out


def load_data(path: str) -> Platform:
    with open(path, "r") as f:
        raw = f.read()
    return Platform(raw)


def run(data: Platform) -> int:
    return data.get_load()


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 136


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
