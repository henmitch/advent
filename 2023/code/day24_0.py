"""https://adventofcode.com/2023/day/24"""
from __future__ import annotations

import itertools
from dataclasses import dataclass
from numbers import Number

import boilerplate as bp

Pair = tuple[Number, Number]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

DEFAULT_LIMITS = (200_000_000_000_000, 400_000_000_000_000)


class Vector(tuple):

    def __add__(self, other: Vector) -> Vector:
        if len(self) != len(other):
            raise ValueError(f"Can't add vectors {self} and {other} "
                             "of different lengths")
        new_values = tuple(a + b for a, b in zip(self, other))
        return Vector(new_values)

    def __sub__(self, other: Vector) -> Vector:
        if len(self) != len(other):
            raise ValueError(f"Can't subtract vectors {self} and {other} "
                             "of different lengths")
        new_values = tuple(a - b for a, b in zip(self, other))
        return Vector(new_values)

    def __rmul__(self, other: int) -> Vector:
        new_values = tuple(other*v for v in self)
        return Vector(new_values)

    def __eq__(self, other: Vector) -> tuple[bool, ...]:
        return tuple(v == o for v, o in zip(self, other))

    def __gt__(self, other: Vector) -> tuple[bool, ...]:
        return tuple(v > o for v, o in zip(self, other))

    def __lt__(self, other: Vector) -> tuple[bool, ...]:
        return tuple(v < o for v, o in zip(self, other))

    def __rmatmul__(self, matrix: list[list]) -> Vector:
        out = []
        for row in matrix:
            out.append(sum(a*b for a, b in zip(self, row)))
        return Vector(out)

    def __truediv__(self, other: Number) -> Vector:
        return Vector((a/other for a in self))

    def midpoint(self, other: Vector) -> Vector:
        return 0.5*(self + other)

    def compare(self, other: Vector) -> Vector:
        return Vector(cmp(a, b) for a, b in zip(self, other))

    def cross(self, other: Vector) -> Vector:
        """Cross product of self and other"""
        x = self[1]*other[2] - self[2]*other[1]
        y = self[2]*other[0] - self[0]*other[2]
        z = self[0]*other[1] - self[1]*other[0]
        return Vector((x, y, z))

    def dot(self, other: Vector) -> Number:
        return sum(s*o for s, o in zip(self, other))

    def is_parallel(self, other: Vector) -> bool:
        return len(set(s/o for s, o in zip(self, other))) == 1


@dataclass
class Stone:
    start: Vector
    v: Vector
    limits: tuple[int, int] = DEFAULT_LIMITS

    def __post_init__(self) -> None:
        if self.limits is None:
            self.limits = DEFAULT_LIMITS
        self.time = self._find_exit_time()
        self.end = self[self.time]

    def __getitem__(self, time: Number) -> Vector:
        return self.start + time*self.v

    def __repr__(self) -> str:
        return (f"{", ".join(str(v) for v in self.start)} @ "
                f"{", ".join(str(v) for v in self.v)}")

    def _find_exit_time(self) -> int:
        # Theoretical limit is the distance from one corner to another, so we
        # set our starting estimate to that squared, because I'm too lazy to
        width = self.limits[1] - self.limits[0]
        out = 3*width**2
        for pos, vel in zip(self.start, self.v):
            if vel == 0:
                continue
            endpoint = self.limits[0]
            if vel > 0:
                endpoint = self.limits[1]
            out = min(out, (endpoint - pos)/vel)

        return out

    def find_time(self, position: Number, dim: int) -> int:
        return (position - self.start[dim])/self.v[dim]

    def intersect_1d(self, other: Stone,
                     dim: int) -> tuple[Number, Number] | None:
        # The endpoints over which they intersect in one given dimension
        mine = sorted((self.start[dim], self.end[dim]))
        theirs = sorted((other.start[dim], other.end[dim]))
        if not does_overlap(mine, theirs):
            return None
        return (
            max(self.limits[0], min(mine), min(theirs)),
            min(self.limits[1], max(mine), max(theirs)),
        )

    def intersect_3d(self, other: Stone) -> tuple[Pair, Pair] | None:
        times_s = []
        times_o = []
        for dim in range(3):
            overlap = self.intersect_1d(other, dim)
            if overlap is None:
                return False
            start_time_s, end_time_s = (self.find_time(p, dim)
                                        for p in overlap)
            times_s.append((start_time_s, end_time_s))
            start_time_o, end_time_o = (other.find_time(p, dim)
                                        for p in overlap)
            times_o.append((start_time_o, end_time_o))
            # Check to see if the relationship between the two actually changed
            # over the course of that trip
            # We need to actually cross
            if all(self[start_time_s].compare(other[start_time_o]) ==
                   self[end_time_s].compare(other[end_time_o])):
                return False
        for t1, t2 in itertools.combinations(times_s, 2):
            if not does_overlap(t1, t2):
                return False

        for t1, t2 in itertools.combinations(times_o, 2):
            if not does_overlap(t1, t2):
                return False

        return True


class Stone2D(Stone):

    def __post_init__(self) -> None:
        super().__post_init__()
        self.start = self[self._find_entry_time()]

    def _find_entry_time(self) -> int:
        t = 0
        for dim in range(3):
            if self.limits[0] < self.start[dim] < self.limits[1]:
                continue
            intersections = [
                self.find_time(limit, dim) for limit in self.limits
            ]
            t = max(t, min(intersections))
        return t


def does_overlap(a: Pair, b: Pair) -> bool:
    return not (min(a) > max(b) or max(a) < min(b))


def cmp(a: Number, b: Number) -> int:
    if a < b:
        return -1
    if a == b:
        return 0
    return 1


def load_data(path: str, limits: tuple[int, int, int] = None) -> list[Stone]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    # pylint: disable=no-value-for-parameter
    stones = [Stone2D(*_parse(line), limits) for line in raw]
    return stones


def _parse(line: str) -> list[Vector, Vector]:
    p, v = line.split(" @ ")
    out = []
    for x in [p, v]:
        x = x.split(", ")
        # Just repeat the y for the z
        out.append(Vector((int(x[0]), int(x[1]), int(x[1]))))
    return out


def run(data: list[Stone2D]) -> int:
    out = 0
    for s1, s2 in itertools.combinations(data, 2):
        if s1.intersect_3d(s2):
            out += 1
    return out


def test():
    data = load_data(TEST_PATH, limits=(7, 27, 0))
    assert run(data) == 2


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
