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


def round_trip(data: dict[str, Cave],
               exclude: list[Cave] = None) -> dict[Pair, int]:
    if exclude is None:
        exclude = []
    distances = shortest_distances(data)
    # Add the minimum distance to a valve that has some flow rate
    for cave in data.values():
        if not cave.rate:
            continue
        to_reaches = [
            distances[k] - 1 for k in distances
            if k[0] is cave and k[1] not in exclude
        ]
        if to_reaches:
            m = min(to_reaches)
        else:
            m = 1000
        for k in distances:
            if cave is k[1]:
                distances[k] += m
    return distances


def find_path(
    data: dict[str, Cave],
    duration: int = 30
) -> tuple[dict[tuple[Cave, ...], tuple[int, int, int]], list[Cave]]:
    distances = shortest_distances(data)

    to_check = [(data["AA"], )]
    # Path: (pressure per time, time, total pressure)
    scores = {(data["AA"], ): (data["AA"].rate, 0, 0)}

    while to_check:
        checking = to_check.pop(0)
        for pair in distances:
            if pair[0] is not checking[-1] or pair[1] in checking:
                continue
            to_add = checking + (pair[1], )
            rate, time, pressure = scores[checking]
            if time >= duration:
                continue
            new_rate = rate + pair[1].rate
            new_time = time + distances[pair]
            new_pressure = pressure + rate*distances[pair]
            scores[to_add] = (new_rate, new_time, new_pressure)
            to_check.append(to_add)

    for path, score in scores.items():
        scores[path] = (score[0], duration,
                        score[2] + score[0]*(duration - score[1]))

    return scores, max(scores, key=lambda x: scores[x][-1])


def run(data: dict[str, Cave], duration: int = 30) -> int:
    d, path = find_path(data, duration)
    return d[path][2]


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 1651


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
