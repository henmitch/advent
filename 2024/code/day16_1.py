"""https://adventofcode.com/2024/day/16"""
from __future__ import annotations

import heapq
from math import inf

import boilerplate as bp
from day16_0 import (DATA_PATH, TEST_PATH_0, TEST_PATH_1, State, load_data,
                     manhattan)


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
                print(f"Found minimum path with score {score}")
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

    def is_corner(self, loc: complex) -> bool:
        return not (loc+1j in self.walls and loc-1j in self.walls) or not (loc+1 in self.walls and loc-1 in self.walls)

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
            # if loc == self.end and score <= end_score:
            #     print(f"Found path with score {score}")
            #     out.append(path[1:])
            #     continue

            step = loc - path[-2]
            nexts = [(step, 1), (step*1j, 1001), (step* -1j, 1001)]
            # is_corner = loc+step*1j in self.walls or loc+step* -1j in self.walls
            for d, d_score in nexts:
                new_loc = loc + d
                new_score = score + d_score

                if new_loc == self.end:
                    print(f"Found path with score {new_score}")
                    out.append(path[1:])
                    break

                if new_loc in path[1:-1]:
                    print("Intersection")
                    continue

                if new_loc in self.walls:
                    print("Wall")
                    continue

                if new_score > min_scores.get(new_loc, inf) and not self.is_corner(new_loc):
                    print("Score too high")
                    continue

                if new_score > end_score:
                    print("Score above end")
                    continue

                print(path, new_loc, new_score)
                min_scores[new_loc] = new_score
                heapq.heappush(
                    q,
                    State(manhattan(new_loc, self.end), new_score, new_loc,
                          path + [new_loc]))

        return out

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

def run(data: Grid) -> int:
    paths = data.find_paths()
    points = {p for path in paths for p in path}
    return len(points)


def test():
    data = load_data(TEST_PATH_0)
    assert run(data) == 45
    print()
    data = load_data(TEST_PATH_1)
    assert run(data) == 64


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    print("tests pass")
    main()
