"""https://adventofcode.com/2023/day/3"""
from __future__ import annotations

import itertools

import boilerplate as bp
from day03_0 import NUMBERS, load_data

Coordinates = tuple[int, int]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class Part:

    def __init__(self, value: str, coords: set[Coordinates]) -> None:
        self.value = int(value) if value.isnumeric() else value
        self.coords = coords
        self.surroundings = self.get_surroundings()

    def __repr__(self) -> str:
        return f"Part {str(self.value)}"

    def __eq__(self, other: Part) -> bool:
        return self.value == other.value and self.coords == other.coords

    def is_adjacent_to(self, other: Part) -> bool:
        return bool(self.surroundings & other.coords)

    def get_surroundings(self) -> set[Coordinates]:
        out = set()
        for x, y in self.coords:
            out |= {(x + i, y + j)
                    for i, j in itertools.product((-1, 0, 1), (-1, 0, 1))}
        return out

    def is_number(self) -> bool:
        return isinstance(self.value, int)


def identify_parts(data: list[str]) -> list[Part]:
    out = []
    width = len(data[0])
    for row_num, row in enumerate(data):
        col_num = 0
        while col_num < width:
            char = row[col_num]
            if char == ".":
                col_num += 1
                continue
            if char not in NUMBERS:
                out.append(Part(char, {(col_num, row_num)}))
                col_num += 1
                continue
            current_num = ""
            coords = []
            while col_num < width and row[col_num] in NUMBERS:
                current_num += row[col_num]
                coords.append((col_num, row_num))
                col_num += 1
            out.append(Part(current_num, set(coords)))
    return out


def run(data: list[str]) -> int:
    out = 0
    parts = identify_parts(data)
    # This will be inefficient, but that's fine
    for part in parts:
        if part.value != "*":
            continue
        adjacents: list[Part] = []
        for other in parts:
            if not other.is_number():
                continue
            if part.is_adjacent_to(other):
                adjacents.append(other)
        if len(adjacents) == 2:
            out += adjacents[0].value*adjacents[1].value
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 467835


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
