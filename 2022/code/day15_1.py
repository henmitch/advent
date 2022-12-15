"""https://adventofcode.com/2022/day/15"""
from functools import reduce
from operator import or_

import boilerplate as bp
from day15_0 import (DATA_PATH, TEST_PATH, Pair, Space, distance, length,
                     load_data)


def limit(num: int, upper: int, lower: int = 0) -> int:
    return max(lower, min(upper, num))


def border(center: complex, radius: int, size: int) -> set[complex]:
    """The nearest points outside a Manhattan circle"""
    radius = length(radius - center)
    x0, y0 = int(center.real), int(center.imag)
    xr, yr = limit(x0 + radius + 1, size), limit(y0, size)
    xt, yt = limit(x0, size), limit(y0 + radius + 1, size)
    xl, yl = limit(x0 - radius - 1, size), limit(y0, size)
    xb, yb = limit(x0, size), limit(y0 - radius - 1, size)
    top_right = list(
        complex(x, y) for x, y in zip(range(xr, xt, -1), range(yr, yt)))
    top_left = list(
        complex(x, y) for x, y in zip(range(xt, xl, -1), range(yt, yl, -1)))
    bottom_left = list(
        complex(x, y) for x, y in zip(range(xl, xb), range(yl, yb, -1)))
    bottom_right = list(
        complex(x, y) for x, y in zip(range(xb, xr), range(yb, yr)))
    return top_right + top_left + bottom_left + bottom_right


def inside(point: complex, circle: Pair) -> bool:
    return distance(point, circle[0]) <= distance(*circle)


def run(space: Space, max_: int):
    for line in space:
        for point in border(*line, max_):
            for pair in space:
                if inside(point, pair):
                    break
            else:
                return int(4_000_000*point.real + point.imag)


def test():
    data = load_data(TEST_PATH)
    assert run(data, 20) == 56000011


def main():
    data = load_data(DATA_PATH)
    print(run(data, 4_000_000))


if __name__ == "__main__":
    test()
    main()
