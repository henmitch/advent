"""https://adventofcode.com/2024/day/14"""
import re
from collections import Counter
from functools import reduce
from operator import mul

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

DEFAULT_WIDTH = 101
DEFAULT_HEIGHT = 103


class Robot:

    def __init__(self, p0: tuple[int, int], v: tuple[int, int], width, height):
        self.p0 = p0
        self.v = v
        self.width = width
        self.height = height

    def position(self, t: int) -> tuple[int, int]:
        return ((self.p0[0] + self.v[0]*t)%self.width,
                (self.p0[1] + self.v[1]*t)%self.height)


def quadrant(p: tuple[int, int], width: int, height: int) -> tuple[int, int]:
    if p[0] == width//2 or p[1] == height//2:
        return -1, -1

    return int(p[0] > width//2), int(p[1] > height//2)


def load_data(path: str,
              width: int = DEFAULT_WIDTH,
              height: int = DEFAULT_HEIGHT) -> list[Robot]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return [parse(line, width, height) for line in raw]


def parse(line: str, width: int, height: int) -> Robot:
    px, py, vx, vy = map(int, re.findall(r"-?\d+", line))
    return Robot((px, py), (vx, vy), width=width, height=height)


def run(data: list[Robot]) -> int:
    quadrants = Counter(
        quadrant(bot.position(100), bot.width, bot.height) for bot in data)
    del quadrants[-1, -1]

    return reduce(mul, quadrants.values())


def test():
    data = load_data(TEST_PATH, width=11, height=7)
    assert run(data) == 12


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
