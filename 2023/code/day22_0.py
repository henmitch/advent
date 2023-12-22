"""https://adventofcode.com/2023/day/22"""
from __future__ import annotations

import itertools
from functools import reduce
from operator import or_, sub
from typing import Iterator

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

Pair = tuple[int, int]
Triple = tuple[int, int, int]


class Brick:

    def __init__(self, start: Triple, end: Triple) -> None:
        # Make it so that start is always less than end
        self.x = tuple(sorted((start[0], end[0])))
        self.length = -sub(*self.x) + 1
        self.y = tuple(sorted((start[1], end[1])))
        self.width = -sub(*self.y) + 1
        self.z = tuple(sorted((start[2], end[2])))
        self.height = -sub(*self.z) + 1
        self.start, self.end = zip(self.x, self.y, self.z)

    def __lt__(self, other: Brick) -> bool:
        if self.z > other.z:
            return False
        if self.z == other.z:
            if self.y > other.y:
                return False
            if self.y == other.y:
                if self.x > other.x:
                    return False
        return True

    def __eq__(self, other: Brick) -> bool:
        return (self.start, self.end) == (other.start, other.end)

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    # yapf: disable
    def __repr__(self) -> str:
        return (f"{",".join(str(x) for x in self.start)}~"
                f"{",".join(str(e) for e in self.end)}")
    # yapf: enable

    def __iter__(self) -> Iterator[Triple]:
        yield from itertools.product(range(self.z[0], self.z[1] + 1),
                                     range(self.y[0], self.y[1] + 1),
                                     range(self.x[0], self.x[1] + 1))

    def is_directly_over(self, other: Brick) -> bool:
        return (overlap(self.x, other.x) and overlap(self.y, other.y)
                and self.z[0] > other.z[1])

    def is_directly_under(self, other: Brick) -> bool:
        return other.is_directly_over(self)

    def is_supported_by(self, other: Brick) -> bool:
        return self.z[0] == other.z[1] + 1 and self.is_directly_over(other)

    def supports(self, other: Brick) -> bool:
        return other.is_supported_by(self)

    def is_grounded(self) -> bool:
        return self.z == (1, 1)

    def ground_beneath(self) -> Brick:
        return Brick(self.start[:2] + (0, ), self.end[:2] + (0, ))

    def drop(self, landscape: list[Brick]) -> Brick:
        h = max(brick.z[1] + 1
                for brick in landscape + [self.ground_beneath()]
                if self.is_directly_over(brick))
        return Brick(self.start[:2] + (h, ),
                     self.end[:2] + (h + self.height - 1, ))


def overlap(a: Pair, b: Pair) -> bool:
    return (a[0] <= b[0] <= a[1] or a[0] <= b[1] <= a[1]
            or b[0] <= a[0] <= b[1] or b[0] <= a[1] <= b[1])


def load_data(path: str) -> list[Brick]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return [Brick(*_parse(line)) for line in raw]


def _parse(line: str) -> tuple[Triple, Triple]:
    start, end = line.split("~")
    start = tuple(int(v) for v in start.split(","))
    end = tuple(int(v) for v in end.split(","))
    # Check if there's any diagonalling going on
    if sum(s != e for s, e in zip(start, end)) > 1:
        raise NotImplementedError(f"Found diagonal brick {line}")
    return start, end


def drop_all(bricks: list[Brick]) -> list[Brick]:
    out = []
    for brick in sorted(bricks):
        out.append(brick.drop(out))
    return out


def deletable(bricks: list[Brick]) -> set[Brick]:
    supporters = {}
    tops = set(bricks)
    for brick, friend in itertools.combinations(bricks, 2):
        if friend.supports(brick):
            supporters[brick] = supporters.get(brick, set()) | {friend}
            tops -= {friend}
        if brick.supports(friend):
            supporters[friend] = supporters.get(friend, set()) | {brick}
            tops -= {brick}
    redundancies = reduce(or_, [v for v in supporters.values() if len(v) > 1])
    singles = reduce(or_, [v for v in supporters.values() if len(v) == 1])
    redundancies -= singles
    return redundancies | tops


def pretty_print(bricks: list[Brick]) -> str:
    min_x, max_x = 0, 0
    min_y, max_y = 0, 0
    max_z = 0
    for brick in bricks:
        min_x = min(min_x, brick.x[0])
        max_x = max(max_x, brick.x[1])
        min_y = min(min_y, brick.y[0])
        max_y = max(max_y, brick.y[1])
        max_z = max(max_z, brick.z[1])
    out_x = [[" " for _ in range(min_x, max_y + 1)] for _ in range(max_z)]
    out_y = [[" " for _ in range(min_y, max_y + 1)] for _ in range(max_z)]
    for brick in bricks:
        for z, y, x in brick:
            out_x[z - 1][x - min_x] = "#"
            out_y[z - 1][y - min_y] = "#"
    out_x = [len(out_x[0])*"-"] + out_x
    out_x = "\n".join("".join(line) for line in reversed(out_x))
    out_y = [len(out_y[0])*"-"] + out_y
    out_y = "\n".join("".join(line) for line in reversed(out_y))
    return out_x + "\n\n" + out_y


def run(data: list[Brick]) -> int:
    return len(deletable(drop_all(data)))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 5


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()

# 947 too high
# 531 too high
# 512 too high
