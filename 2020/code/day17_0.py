"""https://adventofcode.com/2020/day/17"""
from typing import Set, Tuple
import itertools
import boilerplate as bp

Point = Tuple[int, int, int]
Space = Set[Point]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> Space:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    out = set()
    for y, row in enumerate(raw):
        for x, val in enumerate(row):
            if val == "#":
                out.add((x, y, 0))
    return out


def adjacents(point: Point) -> Space:
    out = set(itertools.product(*[[idx - 1, idx, idx + 1] for idx in point]))
    out -= {point}
    return out


def step(space: Space) -> Space:
    out = set()
    for point in space:
        primary_adj = adjacents(point)
        if len(primary_adj & space) in [2, 3]:
            out.add(point)

        for adj in primary_adj:
            secondary_adj = adjacents(adj)
            if len(secondary_adj & space) == 3:
                out.add(adj)

    return out


def run(space: Space, n_times: int = 6) -> int:
    for _ in range(n_times):
        space = step(space)
    return len(space)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 112


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(run(data))
