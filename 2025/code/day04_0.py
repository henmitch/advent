"""https://adventofcode.com/2025/day/4"""
from __future__ import annotations

from collections.abc import Iterable
from itertools import product

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> Floor:
    with open(path, "r") as f:
        raw = f.read().strip()
    return Floor(raw)


class Floor:

    def __init__(self, grid: str):
        self.grid = grid.splitlines()
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def __getitem__(self, pos: complex) -> str:
        if self.oob(pos):
            raise IndexError("Position out of bounds")
        return self.grid[int(pos.imag)][int(pos.real)%len(self.grid[0])]

    def __iter__(self) -> Iterable[tuple[complex, str]]:
        for y in range(self.height):
            for x in range(self.width):
                yield complex(x, y), self[complex(x, y)]

    def oob(self, pos: complex) -> bool:
        return not ((0 <= int(pos.imag) < self.height) and
                    (0 <= int(pos.real) < self.width))

    def neighbors(self, pos: complex) -> list[str]:
        out = []
        for delta in product([-1, 0, 1], repeat=2):
            if delta == (0, 0):
                continue
            new_pos = complex(pos.real + delta[0], pos.imag + delta[1])
            if self.oob(new_pos):
                continue
            out.append(self[new_pos])
        return out

    def is_accessible(self, pos: complex) -> bool:
        return self.neighbors(pos).count("@") < 4


def run(data: Floor) -> int:
    accessible_count = sum(1 for pos, cell in data
                           if cell == "@" and data.is_accessible(pos))
    return accessible_count


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 13


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
