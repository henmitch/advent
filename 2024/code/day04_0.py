"""https://adventofcode.com/2024/day/4"""
from typing import Iterator

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class Search:

    CARDINALS = [1, 1j, -1, -1j]
    DIAGONALS = [1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]
    DIRECTIONS = CARDINALS + DIAGONALS

    def __init__(self, grid: list[str]) -> None:
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)

    def __iter__(self) -> Iterator[tuple[complex, str]]:
        for y in range(self.height):
            for x in range(self.width):
                loc = x + y*1j
                yield loc, self[loc]

    def __getitem__(self, key: complex) -> str:
        return self.grid[int(key.imag)][int(key.real)]

    def oob(self, key: complex) -> bool:
        return not (0 <= key.imag < self.height and 0 <= key.real < self.width)

    def neighbors(self, key: complex) -> Iterator[tuple[complex, complex]]:
        for d in Search.CARDINALS:
            if not self.oob(key + d):
                yield d, key + d

    def xmases(self, key: complex) -> list[tuple[complex, ...]]:
        out = []
        if self[key] != "X":
            return []
        for direction in Search.DIRECTIONS:
            checking = [key]
            for step, letter in enumerate("MAS"):
                loc = key + direction*(step + 1)
                if self.oob(loc) or self[loc] != letter:
                    break
                checking.append(loc)
            else:
                out.append(tuple(checking))
        return out


def load_data(path: str) -> Search:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return Search(raw)


def pretty_print(data: Search, greens: list[complex] = None) -> str:
    if greens is None:
        greens = []
    out = ""
    for loc, letter in data:
        if loc in greens:
            out += bp.colors.GREEN + letter + bp.colors.END
        else:
            out += letter
        if loc.real == data.width - 1:
            out += "\n"
    return out


def run(data: Search) -> int:
    xmases = []
    for loc, _ in data:
        xmases += data.xmases(loc)
    out = len(xmases)
    locs = [loc for xmas in xmases for loc in xmas]
    print(pretty_print(data, locs))
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 18


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
