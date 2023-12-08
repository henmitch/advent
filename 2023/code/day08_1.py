"""https://adventofcode.com/2023/day/8"""
import re
from functools import reduce
from itertools import cycle
from math import lcm
from operator import or_

import boilerplate as bp

TEST_PATH = bp.get_test_path("1")
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[int, dict[str, tuple[str, str]]]:
    with open(path, "r") as f:
        dirs, _, *nodes = f.read().splitlines()
    dirs = list(map(int, dirs.replace("L", "0").replace("R", "1")))
    nodes = reduce(or_, (_parse(line) for line in nodes))
    return dirs, nodes


def _parse(line: str) -> dict[str, tuple[str, str]]:
    fmt = r"(\w{3}) = \((\w{3}), (\w{3})\)"
    node, l, r = re.match(fmt, line).groups()
    return {node: (l, r)}


def cycle_length(dirs: list[int], nodes: dict[str, tuple[str, str]],
                 start: str) -> int:
    out = 0
    current = start
    for dir_ in cycle(dirs):
        current = nodes[current][dir_]
        out += 1
        if current[-1] == "Z":
            break
    return out


def run(data: tuple[list[int], dict[str, tuple[str, str]]]) -> int:
    dirs, nodes = data
    starts = [node for node in nodes.keys() if node[-1] == "A"]
    lengths = [cycle_length(dirs, nodes, start) for start in starts]
    out = lcm(*lengths)
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 6


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
