"""https://adventofcode.com/2022/day/8"""
import itertools
from day08_0 import DATA_PATH, TEST_PATH, load_data


def scenic_score(data: list[list[int]], x: int, y: int) -> int:
    v = data[y][x]
    t = b = l = r = 1
    # Top
    for i in range(y - 1, 0, -1):
        if data[i][x] >= v:
            break
        t += 1
    # Bottom
    for i in range(y + 1, len(data) - 1):
        if data[i][x] >= v:
            break
        b += 1
    # Left
    for i in range(x - 1, 0, -1):
        if data[y][i] >= v:
            break
        l += 1
    # Right
    for i in range(x + 1, len(data[0]) - 1):
        if data[y][i] >= v:
            break
        r += 1
    return t*b*l*r


def run(data: list[list[int]]) -> int:
    ry = range(1, len(data) - 1)
    rx = range(1, len(data[0]) - 1)
    return max(scenic_score(data, x, y) for x, y in itertools.product(rx, ry))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 8


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
