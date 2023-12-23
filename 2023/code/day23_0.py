"""https://adventofcode.com/2023/day/23"""
from __future__ import annotations

import itertools
from collections import UserList
from typing import Any, Collection, Iterator, Sequence

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class Segment:

    def __init__(self, start: complex, path: tuple[complex],
                 end: complex) -> None:
        self.start = start
        self.end = end
        self.path = path

    def __repr__(self) -> str:
        return f"{self.start}..{len(self.path)}..{self.end}"

    def __add__(self, other: Segment) -> Segment:
        if not self.is_contiguous_with(other):
            raise ValueError("Cannot add non-contiguous segments "
                             f"{self} and {other}")
        return Segment(self.start, self.path + other.path, other.end)

    def __len__(self) -> int:
        return len(self.path)

    def __iter__(self) -> Iterator[complex]:
        yield from self.path

    def __lt__(self, other: Segment | None) -> Segment:
        # To work with heapq, we need longer-length segments to have higher
        # priority
        if other is None:
            return True
        return len(self) > len(other)

    def is_contiguous_with(self, other: Segment) -> bool:
        return are_adjacent(self.end, other.start)

    def find_nexts(self, others: Collection[Segment]) -> list[Segment]:
        return sorted(other for other in others
                      if self.is_contiguous_with(other)
                      and not self.overlaps_with(other))

    def overlaps_with(self, other: Segment) -> bool:
        return bool(set(self.path) & set(other.path))


class IcyMaze(UserList):

    def __init__(self, data: Sequence[Sequence]) -> None:
        if not data:
            self.data = [[]]
        self.height = len(data)
        self.width = len(data[0])
        self.start = complex(data[0].index("."), 0)
        self.end = complex(data[-1].index("."), self.height - 1)
        super().__init__(data)
        self._hash = hash(str(self))
        self.slopes = self.get_slopes()

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

    def neighbors(self, loc: complex) -> set[complex]:
        if self[loc] == ">":
            return {loc + 1}
        if self[loc] == "v":
            return {loc + 1j}
        if self[loc] == "<":
            return {loc - 1}
        if self[loc] == "^":
            return {loc - 1j}
        return {
            loc + d
            for d in [1, 1j, -1, -1j]
            if not self.oob(loc + d) and self[loc + d] != "#"
        }

    def get_slopes(self) -> set[complex]:
        return {loc for loc, char in self.all_points() if char in ">v<^"}

    def find_next_slope(
            self,
            loc: complex,
            seen: tuple[complex] = None) -> set[tuple[complex, ...]]:
        if seen is None:
            seen = ()
        if loc in self.slopes:
            return [seen]
        if loc == self.end:
            return [seen + (loc, )]

        out: set[tuple[complex, ...]] = set()
        for neighbor in self.neighbors(loc):
            if neighbor not in seen:
                for path in self.find_next_slope(neighbor, seen + (loc, )):
                    out.add(path)
        return out

    def get_segments(self) -> set[Segment]:
        out = set()
        for slope in self.slopes | {self.start}:
            neighbor = self.neighbors(slope).pop()
            paths = self.find_next_slope(neighbor, (slope, ))
            for path in paths:
                out.add(Segment(slope, path, path[-1]))
        return out

    def pretty_print(self,
                     points: dict[complex, str] | set[complex] = None) -> str:
        if points is None:
            points = {}
        elif not isinstance(points, dict):
            points = {point: "O" for point in points}
        out = ""
        for y, row in enumerate(self):
            for x, char in enumerate(row):
                if complex(x, y) in points:
                    out += points[complex(x, y)]
                else:
                    out += char
            out += "\n"
        return out.strip()

    def find_longest_path(self) -> set[Segment]:
        out = set()
        segments = self.get_segments()
        to_add = {seg for seg in segments if seg.start == self.start}
        while to_add:
            adding = to_add.pop()
            if adding.start == self.start and adding.end == self.end:
                out.add(adding)
                continue
            for friend in adding.find_nexts(segments):
                if adding.overlaps_with(friend):
                    continue
                to_add.add(adding + friend)
        return out


def are_adjacent(a: complex, b: complex) -> bool:
    return abs(a - b) == 1


def follow(mapping: dict[Segment, set[Segment]],
           start: Segment) -> set[Segment]:
    if start not in mapping:
        return set()
    out = set()
    for friend in mapping[start]:
        for segment in follow(mapping, friend):
            out.add(start + friend + segment)
    return out


def load_data(path: str) -> IcyMaze:
    with open(path, "r") as f:
        data = f.read().splitlines()
    return IcyMaze(data)


def run(data: IcyMaze) -> int:
    all_paths = data.find_longest_path()
    return max(len(path) for path in all_paths) - 1


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 94


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
