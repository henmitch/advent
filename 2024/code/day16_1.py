"""https://adventofcode.com/2024/day/16"""
from __future__ import annotations

import heapq
from math import inf

import boilerplate as bp
from day16_0 import DATA_PATH, TEST_PATH_0, TEST_PATH_1, Grid, State, manhattan


class GridWithPaths(Grid):

    def is_corner(self, loc: complex) -> bool:
        return (not (loc + 1j in self.walls and loc - 1j in self.walls)
                or not (loc + 1 in self.walls and loc - 1 in self.walls))

    def estimated_distance(self, loc: complex) -> int:
        turns = int(loc.real != self.end.real or loc.imag != self.end.imag)
        return manhattan(loc, self.end) + 1000*turns

    def find_paths(self) -> list[list[complex]]:
        end_score, _ = self.walk()
        out = []
        q = [
            State(manhattan(self.start, self.end), 0, self.start,
                  [self.start - 1, self.start])
        ]
        min_scores = {self.start: 0}

        while q:
            score, loc, path = heapq.heappop(q)

            step = loc - path[-2]
            nexts = [(step, 1), (step*1j, 1001), (step* -1j, 1001)]
            for d, d_score in nexts:
                new_loc = loc + d
                new_score = score + d_score

                if new_loc == self.end:
                    out.append(path[1:] + [new_loc])
                    break

                if new_loc in path[1:-1]:
                    continue

                if new_loc in self.walls:
                    continue

                if new_score > end_score:
                    continue

                if (new_score > min_scores.get(new_loc, inf)
                        and not self.is_corner(new_loc)):
                    continue

                min_scores[new_loc] = new_score
                heapq.heappush(
                    q,
                    State(self.estimated_distance(new_loc), new_score, new_loc,
                          path + [new_loc]))

        return out


def load_data(path: str) -> GridWithPaths:
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
    return GridWithPaths(walls, start, end)


def run(data: GridWithPaths) -> int:
    paths = data.find_paths()
    points = {p for path in paths for p in path}
    return len(points)


def test():
    data = load_data(TEST_PATH_0)
    assert run(data) == 45
    print("Passed first test")
    data = load_data(TEST_PATH_1)
    assert run(data) == 64
    print("Passed second test")


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    print("Tests pass")
    main()
