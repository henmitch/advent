"""https://adventofcode.com/2022/day/15"""
import re
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

Pair = tuple[complex, complex]
Space = list[Pair]


def parse(line: str) -> Pair:
    r = (r"x=(?P<xs>-?\d+), y=(?P<ys>-?\d+).*x=(?P<xb>-?\d+), y=(?P<yb>-?\d+)")
    m = re.search(r, line).groupdict()
    return int(m["xs"]) + int(m["ys"])*1j, int(m["xb"]) + int(m["yb"])*1j


def load_data(path: str) -> Space:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return [parse(line) for line in raw]


def distance(p1: complex, p2: complex) -> int:
    return abs(p1.real - p2.real) + abs(p1.imag - p2.imag)


def length(p: complex) -> int:
    return int(abs(p.real) + abs(p.imag))


def bounds(space: Space) -> Pair:
    top = bottom = left = right = 0
    for sensor, beacon in space:
        l = length(beacon)
        if (new_top := (sensor.imag + l)) > top:
            top = new_top
        if (new_bottom := (sensor.imag - l)) < bottom:
            bottom = new_bottom
        if (new_left := (sensor.real - l)) < left:
            left = new_left
        if (new_right := (sensor.real + l)) > right:
            right = new_right
    return left + top*1j, right + bottom*1j


def spaces_in_row(space: Space, row: int) -> int:
    out = 0
    top_left, bottom_right = bounds(space)
    for x in range(int(top_left.real), int(bottom_right.real) + 1):
        pos = x + row*1j
        to_add = 0
        for sensor, beacon in space:
            if pos in {sensor, beacon}:
                to_add = 0
                break
            if distance(sensor, pos) <= distance(sensor, beacon):
                to_add = 1
        out += to_add
    return out


def test():
    data = load_data(TEST_PATH)
    assert spaces_in_row(data, 10) == 26


def main():
    data = load_data(DATA_PATH)
    print(spaces_in_row(data, 2_000_000))


if __name__ == "__main__":
    test()
    # main()
