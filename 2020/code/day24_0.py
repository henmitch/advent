"""https://adventofcode.com/2020/day/24"""
from __future__ import annotations

import re
from numbers import Complex

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

DIRECTIONS = {
    "e": 1 + 0j,
    "se": 0.5 - 0.5j,
    "sw": -0.5 - 0.5j,
    "w": -1 + 0j,
    "nw": -0.5 + 0.5j,
    "ne": 0.5 + 0.5j
}



def load_data(path: str) -> list[list[str]]:
    with open(path, "r") as f:
        raw = f.readlines()
    out = []
    for line in raw:
        out.append(re.findall(r"[ns]?[ew]", line))
    return out


def locate(steps: list[str]) -> Complex:
    return sum(DIRECTIONS[step] for step in steps)


def run(data: list[list[str]]) -> set(Complex):
    flippeds = [locate(line) for line in data]
    final = set()
    for flipped in flippeds:
        if flipped not in final:
            final.add(flipped)
        else:
            final.remove(flipped)
    return final


def test():
    data = load_data(TEST_PATH)
    assert len(run(data)) == 10


def main():
    data = load_data(DATA_PATH)
    print(len(run(data)))


if __name__ == "__main__":
    test()
    main()
