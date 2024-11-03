"""https://adventofcode.com/2023/day/24"""
from __future__ import annotations

from day24_0 import DATA_PATH, TEST_PATH, Stone, Vector


def load_data(path: str, limits: tuple[int, int, int] = None) -> list[Stone]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    # pylint: disable=no-value-for-parameter
    stones = [Stone(*_parse(line), limits) for line in raw]
    return stones


def _parse(line: str) -> list[Vector, Vector]:
    p, v = line.split(" @ ")
    out = []
    for x in [p, v]:
        x = x.split(", ")
        out.append(Vector(int(value) for value in x))
    return out


def frame_shift(stones: list[Stone], x: Vector, v: Vector) -> list[Stone]:
    return [
        Stone(x - stone.start, v - stone.v, stone.limits) for stone in stones
    ]


def run(data: list[Stone]) -> int:
    # Gotten (shamelessly) from:
    # https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/kxqjg33/
    # Shift everything into the reference frame of stone 0
    first = data[0]
    a, b = frame_shift(data[1:3], first.start, first.v)
    # Time of collision with rock a
    ta = -a.start.cross(b.start).dot(b.v)/a.v.cross(b.start).dot(b.v)
    # Time of collision with rock b
    tb = -a.start.cross(b.start).dot(a.v)/a.start.cross(b.v).dot(a.v)

    # Position of collision with rock a
    ca = data[1].start + ta*data[1].v
    # Position of collision with rock b
    cb = data[2].start + tb*data[2].v

    # Velocity of the rock
    v = (cb - ca)/(tb - ta)
    # Initial position of the rock
    p = ca - ta*v

    return sum(p)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 47


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    print()
    main()
