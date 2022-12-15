"""https://adventofcode.com/2022/day/15"""
from functools import reduce
from operator import or_

import boilerplate as bp
from day15_0 import DATA_PATH, TEST_PATH, Pair, Space, load_data, length, distance


def border(center: complex, radius: int) -> set[complex]:
    """The nearest points outside a Manhattan circle"""
    radius = length(radius - center)
    x0, y0 = int(center.real), int(center.imag)
    xr, yr = x0 + radius + 1, y0
    xt, yt = x0, y0 + radius + 1
    xl, yl = x0 - radius - 1, y0
    xb, yb = x0, y0 - radius - 1
    top_right = {
        complex(x, y)
        for x, y in zip(range(xr, xt, -1), range(yr, yt))
    }
    top_left = {
        complex(x, y)
        for x, y in zip(range(xt, xl, -1), range(yt, yl, -1))
    }
    bottom_left = {
        complex(x, y)
        for x, y in zip(range(xl, xb), range(yl, yb, -1))
    }
    bottom_right = {
        complex(x, y)
        for x, y in zip(range(xb, xr), range(yb, yr))
    }
    return top_right | top_left | bottom_left | bottom_right

def inside(point: complex, circle: Pair) -> bool:
    sensor, beacon = circle
    return  distance(point, sensor) <= distance(*circle)

def run(space: Space, max_: int):
    borders = reduce(or_, (border(*line, max_) for line in space))
    for point in borders:
        for pair in space:
            if inside(point, pair):
                break
        else:
            return 4000000*point.real + point.imag


def test():
    data = load_data(TEST_PATH)
    assert run(data, 20) == 56000011
    print("Passed!")


def main():
    data = load_data(DATA_PATH)
    print(run(data, 4000000))


if __name__ == "__main__":
    test()
    main()
