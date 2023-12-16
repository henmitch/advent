"""https://adventofcode.com/2023/day/16"""
import itertools
from collections import UserList, deque
from typing import Any, Iterator, Sequence

import boilerplate as bp

Pair = tuple[complex, complex]

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

    def oob(self, loc: complex) -> bool:
        return (loc.real < 0 or loc.imag < 0 or loc.real >= self.width
                or loc.imag >= self.height)


def load_data(path: str) -> Array:
    with open(path, "r") as f:
        return Array(f.read().splitlines())


def backslash(direction: complex) -> tuple[complex]:
    # Vertical: turn to the left
    if not direction.real:
        out = (direction* -1j, )
    # Horizontal: turn to the right
    elif not direction.imag:
        out = (direction*1j, )
    else:
        raise ValueError(f"Invalid direction: {direction}")
    return out


def slash(direction: complex) -> tuple[complex]:
    # Vertical: turn to the right
    if not direction.real:
        out = (direction*1j, )
    # Horizontal: turn to the left
    elif not direction.imag:
        out = (direction* -1j, )
    else:
        raise ValueError(f"Invalid direction: {direction}")
    return out


def pipe(direction: complex) -> tuple[complex] | Pair:
    # Vertical: leave alone
    if not direction.real:
        out = (direction, )
    # Horizontal: split into up and down
    elif not direction.imag:
        out = (-1j, 1j)
    else:
        raise ValueError(f"Invalid direction: {direction}")
    return out


def dash(direction: complex) -> tuple[complex] | Pair:
    # Vertical:split into left and right
    if not direction.real:
        out = (-1, 1)
    # Horizontal: leave alone
    elif not direction.imag:
        out = (direction, )
    else:
        raise ValueError(f"Invalid direction: {direction}")
    return out


EFFECTS = {"\\": backslash, "/": slash, "|": pipe, "-": dash}


def step(loc: complex, direction: complex, char: str) -> list[Pair]:
    if char == ".":
        return [(loc + direction, direction)]
    new_directions = EFFECTS[char](direction)
    return [(loc + new_dir, new_dir) for new_dir in new_directions]


def find_all_next_beams(map_: Array) -> dict[Pair, list[Pair]]:
    out = {}
    for point, char in map_.all_points():
        for direction in [1, -1j, -1, 1j]:
            next_step = step(point, direction, char)
            next_step = [(next_loc, next_dir)
                         for next_loc, next_dir in next_step
                         if not map_.oob(next_loc)]
            out[(point, direction)] = next_step
    return out


def walk(path: dict[Pair, list[Pair]], start: Pair = (0, 1)) -> set[Pair]:
    seen = set()
    to_check = deque([start])
    while to_check:
        checking = to_check.popleft()
        if checking in path and checking not in seen:
            for next_step in path[checking]:
                to_check.append(next_step)
        seen.add(checking)
    return seen


def count_points(seen: set[Pair]) -> int:
    return len({v for v, _ in seen})


def run(data: Array) -> int:
    all_next_beams = find_all_next_beams(data)
    seen = walk(all_next_beams)
    n_points = count_points(seen)
    return n_points


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 46


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
