"""https://adventofcode.com/2024/day/16"""
from __future__ import annotations

import heapq
from math import inf

import boilerplate as bp
from day16_0 import DATA_PATH, TEST_PATH_0, TEST_PATH_1, Grid, State, manhattan


class GridWithPaths(Grid):

    def __iter__(self):
        for x in range(self.width):
            for y in range(self.height):
                yield x + y*1j

    def neighbors(self, loc: complex) -> list[complex]:
        return [loc + d for d in [1, -1, 1j, -1j] if loc + d not in self.walls]

    def is_dead_end(self, loc: complex) -> bool:
        if loc in self.walls or loc == self.start or loc == self.end:
            return False
        return len(self.neighbors(loc)) == 1

    def is_fork(self, loc: complex) -> bool:
        if loc in self.walls:
            return False
        return len(self.neighbors(loc)) > 2

    def is_bend(self, loc: complex) -> bool:
        neighbors = self.neighbors(loc)
        return len(neighbors) >= 2 and sum(neighbors) != 0

    def find_dead_ends(self) -> set[complex]:
        out = set()
        for loc in self:
            if loc in out or not self.is_dead_end(loc):
                continue
            out.add(loc)
            n = loc
            while not self.is_fork(n) and n not in [self.start, self.end]:
                out.add(n)
                n = (set(self.neighbors(n)) - out).pop()
        print(f"Found {len(out)} dead ends")
        return out

    def find_score(self, path: list[complex]) -> dict[complex, int]:
        out = {loc: 0 for loc in path + [self.start - 1]}
        direction = 1
        for a, b in zip(path, path[1:]):
            if b - a != direction:
                # We've turned
                out[b] = out[a] + 1001
                direction = b - a
            else:
                out[b] = out[a] + 1
        return out

    def estimated_distance(self, loc: complex) -> int:
        turns = int(loc.real != self.end.real or loc.imag != self.end.imag)
        return manhattan(loc, self.end) + 1000*turns

    def find_paths(self) -> list[list[complex]]:
        do_not_enter = self.find_dead_ends() | set(self.walls)
        end_score, example = self.walk()
        print(f"End score: {end_score}")
        out = []
        q = [
            State(manhattan(self.start, self.end), 0, self.start,
                  [self.start - 1, self.start])
        ]
        min_scores = self.find_score(example)

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

                if new_loc in do_not_enter:
                    continue

                if new_score > end_score:
                    continue

                if (new_score > min_scores.get(new_loc, inf)
                        and not self.is_bend(new_loc)):
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
