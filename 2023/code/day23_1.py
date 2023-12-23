"""https://adventofcode.com/2023/day/23"""
from __future__ import annotations

from typing import Sequence

from day23_0 import DATA_PATH, TEST_PATH, IcyMaze, Segment, are_adjacent


class Maze(IcyMaze):

    def __init__(self, data: Sequence[Sequence]) -> None:
        super().__init__(data)
        self.junctions = self.get_junctions()
        self.segments = self.get_segments()

    def neighbors(self, loc: complex) -> set[complex]:
        return {
            loc + d
            for d in [1, 1j, -1, -1j]
            if not self.oob(loc + d) and self[loc + d] != "#"
        }

    def get_junctions(self) -> set[complex]:
        return {
            loc
            for loc, char in self.all_points()
            if char in ".>v<^" and len(self.neighbors(loc)) > 2
        }

    def get_segments(self) -> tuple[Segment, ...]:
        out = set()
        for junction in self.junctions | {self.start}:
            for neighbor in self.neighbors(junction):
                paths = self.find_next_junction(neighbor, (junction, ))
                for path in paths:
                    out.add(Segment(junction, path, path[-1]))
        return tuple(out)

    def find_next_junction(
            self,
            loc: complex,
            seen: tuple[complex] = None) -> set[tuple[complex, ...]]:
        if seen is None:
            seen = ()
        if loc in self.junctions:
            return [seen]
        if loc == self.end:
            return [seen + (loc, )]

        out: set[tuple[complex, ...]] = set()
        for neighbor in self.neighbors(loc):
            if neighbor not in seen:
                for path in self.find_next_junction(neighbor, seen + (loc, )):
                    out.add(path)
        return out

    def find_longest_path(self, so_far: Segment = None) -> Segment:
        if so_far is None:
            so_far = [s for s in self.segments if s.start == self.start][0]
        if so_far.end == self.end:
            print(len(so_far))
            return so_far
        nexts = so_far.find_nexts(self.segments)
        # Dead ends
        if not nexts:
            return Segment(0j, [], 0j)
        return min(
            self.find_longest_path(so_far + neighbor) for neighbor in nexts)

    def adjacent_junction(self, loc: complex) -> complex | None:
        for junction in self.junctions:
            if are_adjacent(loc, junction):
                return junction
        if loc == self.end:
            return loc
        return None


def load_data(path: str) -> Maze:
    with open(path, "r") as f:
        data = f.read().splitlines()
    return Maze(data)


def run(data: Maze) -> int:
    longest_path = data.find_longest_path()
    return len(longest_path) - 1


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 154


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    print("Passed!")
    main()
