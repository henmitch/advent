"""https://adventofcode.com/2024/day/16"""
from __future__ import annotations

import heapq
from dataclasses import dataclass
from math import inf

import boilerplate as bp

TEST_PATH_0 = bp.get_test_path("0")
TEST_PATH_1 = bp.get_test_path("1")
DATA_PATH = bp.get_data_path()


@dataclass(frozen=True)
class State:
    dist: int
    score: int
    location: complex
    path: list[complex]

    def __lt__(self, other: State) -> bool:
        if self.score < other.score:
            return True
        if self.score > other.score:
            return False
        return self.dist < other.dist

    def __iter__(self):
        return iter([self.score, self.location, self.path])


class Grid:

    def __init__(self, walls: list[complex], start: complex,
                 end: complex) -> None:
        self.walls = walls
        self.start = start
        self.end = end
        self.width = max(int(w.real) for w in walls) + 1
        self.height = max(int(w.imag) for w in walls) + 1

    def walk(self) -> tuple[int, list[complex]]:
        q = [
            State(manhattan(self.start, self.end), 0, self.start,
                  [self.start - 1, self.start])
        ]
        min_scores = {self.start: 0}
        while q:
            score, loc, path = heapq.heappop(q)
            if loc == self.end:
                return score, path[1:]

            step = loc - path[-2]
            for d, d_score in [(step, 1), (step*1j, 1001), (step* -1j, 1001)]:
                new_loc = loc + d
                if new_loc in path[1:-1] or new_loc in self.walls:
                    continue
                new_score = score + d_score
                if new_score >= min_scores.get(new_loc, inf):
                    continue
                min_scores[new_loc] = new_score
                heapq.heappush(
                    q,
                    State(manhattan(new_loc, self.end), new_score,new_loc,
                          path + [new_loc]))

        raise RuntimeError("Never reached endpoint")

    def pretty_print(self, path: list[complex]) -> str:
        out = ""
        for y in range(self.height):
            for x in range(self.width):
                loc = x + y*1j
                if loc in self.walls:
                    out += "#"
                elif loc in path:
                    out += "O"
                elif loc == self.start:
                    out += "S"
                elif loc == self.end:
                    out += "E"
                else:
                    out += " "
            out += "\n"
        return out


def load_data(path: str) -> Grid:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    walls = []
    start = 0 + 0j
    end = 0 + 0j
    for y, line in enumerate(raw):
        for x, char in enumerate(line):
            loc = x + y*1j
            if char == "#":
                walls.append(loc)
            elif char == "S":
                start = loc
            elif char == "E":
                end = loc
    return Grid(walls, start, end)


def manhattan(a: complex, b: complex) -> int:
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def run(data: Grid) -> int:
    out = data.walk()
    return out[0]


def test():
    data = load_data(TEST_PATH_0)
    assert run(data) == 7036
    print("Test 0 passed")
    data = load_data(TEST_PATH_1)
    assert run(data) == 11048
    print("Test 1 passed")


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
