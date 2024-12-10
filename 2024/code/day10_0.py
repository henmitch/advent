"""https://adventofcode.com/2024/day/10"""
from typing import Iterator

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class Grid:
    CARDINALS = [1, 1j, -1, -1j]

    def __init__(self, grid: list[list[int]]) -> None:
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

    def neighbors(self, key: complex) -> Iterator[complex]:
        for d in Grid.CARDINALS:
            if not self.oob(key + d):
                yield key + d

    def reachable_tops(self, loc: complex) -> set[complex]:
        if self[loc] == 9:
            return {loc}
        out = set()
        for neighbor in self.neighbors(loc):
            if self[neighbor] == self[loc] + 1:
                out |= self.reachable_tops(neighbor)
        return out


def load_data(path: str) -> Grid:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return Grid([[int(x) for x in row] for row in raw])


def run(data: Grid) -> int:
    out = 0
    for loc, val in data:
        if val == 0:
            out += len(data.reachable_tops(loc))
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 36


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
