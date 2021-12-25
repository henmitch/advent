"""https://adventofcode.com/2021/day/25"""
import boilerplate as bp
from typing import Tuple, List

Point = Tuple[int, int]

DATA_PATH = bp.get_data_path()
TEST_PATH = bp.get_test_path()


class Grid:
    def __init__(self, data: List[List[str]]):
        self.grid = data

    def __getitem__(self, loc: Point) -> str:
        x, y = loc
        return self.grid[y][x]

    def __setitem__(self, loc: Point, val: str):
        x, y = loc
        self.grid[y][x] = val

    def __iter__(self):
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                yield x, y, char

    def __eq__(self, other) -> bool:
        if not isinstance(other, Grid):
            return False
        return self.grid == other.grid

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.grid)

    def next_right(self, loc: Point) -> Point:
        x, y = loc
        if x == len(self.grid[0]) - 1:
            return 0, y
        return x + 1, y

    def next_down(self, loc: Point) -> Point:
        x, y = loc
        if y == len(self.grid) - 1:
            return x, 0
        return x, y + 1

    def is_occupied(self, loc: Point) -> bool:
        x, y = loc
        return self.grid[y][x] != "."

    def will_step_right(self, loc: Point) -> bool:
        if self[loc] == ">" and not self.is_occupied(self.next_right(loc)):
            return True
        return False

    def will_step_down(self, loc: Point) -> bool:
        if self[loc] == "v" and not self.is_occupied(self.next_down(loc)):
            return True
        return False


def empty_grid(width: int, height: int) -> Grid:
    return Grid([[None for _ in range(width)] for _ in range(height)])


def step(grid: Grid):
    intermediate = empty_grid(len(grid.grid[0]), len(grid.grid))
    out = empty_grid(len(grid.grid[0]), len(grid.grid))
    for x, y, cell in grid:
        loc = (x, y)
        if intermediate[loc] is not None:
            continue
        if grid.will_step_right(loc):
            intermediate[loc] = "."
            intermediate[grid.next_right(loc)] = ">"
        else:
            intermediate[loc] = cell

    for x, y, cell in intermediate:
        loc = (x, y)
        if out[loc] is not None:
            continue
        if intermediate.will_step_down(loc):
            out[loc] = "."
            out[intermediate.next_down(loc)] = "v"
        else:
            out[loc] = cell

    return out


def solve(grid: Grid) -> int:
    steps = 0
    while True:
        out = step(grid)
        steps += 1
        if any(any(cell is None for cell in row) for row in out):
            raise ValueError("You missed something.")
        if out == grid:
            return steps

        grid = out


def load_data(path: str) -> List[List[str]]:
    with open(path) as f:
        raw = f.read().splitlines()
    return Grid([list(line) for line in raw])


def test():
    data = load_data(TEST_PATH)
    assert solve(data) == 58


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(solve(data))
