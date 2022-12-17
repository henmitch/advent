"""https://adventofcode.com/2022/day/16"""
from __future__ import annotations

import re
from collections.abc import Iterator
from math import inf
from itertools import product

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class Cave:

    def __init__(self, name: str, rate: int) -> None:
        self.name = name
        self.rate = rate
        self.children: list[Cave] = []

    def __repr__(self) -> str:
        return self.name

    def add_children(self, children: list[Cave]) -> None:
        self.children = list(children)

    def children_worth_visiting(self, path: tuple[Cave]) -> Iterator[Cave]:
        for child in self.children:
            if child in path:
                continue
            yield child


Pair = tuple[Cave, Cave]


def parse(line: str) -> tuple[str, int, list[str]]:
    r = r"(?P<name>[A-Z]{2}).*=(?P<rate>\d+).*valves? (?P<children>[A-Z ,]+)"
    parsed = re.search(r, line)
    children = parsed.group("children").split(", ")
    rate = int(parsed.group("rate"))
    return parsed.group("name"), rate, children


def load_data(path: str) -> dict[str, Cave]:
    with open(path, "r") as f:
        raw = tuple(map(parse, f.read().splitlines()))
    # Instantiate the caves
    out: dict[str, Cave] = {}
    for cave in raw:
        out[cave[0]] = Cave(cave[0], cave[1])
    # Designate their children
    for cave in raw:
        out[cave[0]].add_children([out[i] for i in cave[2]])
    return out


def shortest_distances(data: dict[str, Cave]) -> dict[Pair, int]:
    # Floyd-Warshall algorithm
    caves = [c for c in data.values()]
    tmp: dict[tuple[Cave, Cave], int | float] = {}
    for c1, c2 in product(caves, caves):
        if c1 is c2:
            tmp[(c1, c2)] = 0
        elif c1 in c2.children:
            tmp[(c1, c2)] = 1
        else:
            tmp[(c1, c2)] = inf
    for k in caves:
        for i in caves:
            for j in caves:
                if tmp[(i, j)] > (interim := tmp[(i, k)] + tmp[(k, j)]):
                    tmp[(i, j)] = interim
    # Adding 1 for the turn-the-valve step and removing the caves with 0 values
    out = {}
    for k, v in tmp.items():
        if ((k[0].name == "AA" and k[1].rate > 0)
                or (k[0].rate > 0 and k[1].rate > 0 and k[0] is not k[1])):
            out[k] = v + 1
    return out


def round_trip(data: dict[str, Cave]) -> dict[Pair, int]:
    distances = shortest_distances(data)
    # Add the minimum distance to a valve that has some flow rate
    for cave in data.values():
        for k in distances:
            m = min(distances[k] for k in distances if k[1] is cave)
            if cave is k[1]:
                distances[k] += m
    return distances


def make_matrix(data: dict[Pair, int]) -> dict[Pair, float]:
    # Turning into a bang-to-buck ratio
    return {k: k[1].rate/v for k, v in data.items()}


def mean(nums: list[int | float]) -> float:
    if not nums:
        return 0
    return sum(nums)/len(nums)


def make_roi(matrix: dict[Pair, float],
             exclude: list[Cave] = None) -> dict[str, float]:
    # The expected value of leaving a given cave
    if exclude is None:
        exclude = []
    # Get all the unique cave names:
    caves = {k[0]: [] for k in matrix if k[0] not in exclude}
    # Bang-to-buck ratio of each path from k
    for pair in matrix:
        if pair[0] in exclude or pair[1] in exclude:
            continue
        caves[pair[0]].append(matrix[pair])
    return {k: mean(v) for k, v in caves.items()}


def find_path(data: dict[str, Cave]) -> list[Cave]:
    distances = shortest_distances(data)
    matrix = make_matrix(distances)

    current = data["AA"]
    seen = [current]
    # To make sure we hit every non-zero point once
    l = len([v for v in data.values() if v.rate > 0])
    for _ in range(l):
        roi = make_roi(matrix, exclude=seen)
        max_so_far = 0
        for k, v in matrix.items():
            if k[0] is not current or k[1] in seen:
                continue
            if v + roi[k[1]] > max_so_far:
                next_step = k[1]
                max_so_far = v + roi[k[1]]
        seen.append(next_step)
        current = next_step
    return seen


def run(data: dict[str, Cave], duration: int = 30) -> int:
    path = find_path(data)
    distances = shortest_distances(data)
    pairs = zip(path, path[1:])
    time = 0
    current_rate = 0
    out = 0
    # Until the clock runs out...
    while time < duration:
        try:
            pair = next(pairs)
        except StopIteration:
            time += 1
            # Add the pressure we're currently adding
            out += current_rate
            continue
        # Check and see if we have time to go to the next cave
        distance = distances[pair]
        if time + distance > duration:
            # If we don't, run out the clock
            out += current_rate*(duration - time)
            time = duration
            continue
        # If we do have time to go to the next cave, we do it.
        time += distance
        out += distance*current_rate
        current_rate += pair[1].rate
    return out


def test():
    data = load_data(TEST_PATH)
    out = run(data)
    print(out)


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
