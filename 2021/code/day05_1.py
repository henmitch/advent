"""https://adventofcode.com/2021/day/5"""
import time
from typing import List, Set, Tuple

import boilerplate as bp


DATA_PATH = bp.get_data_path()
TEST_PATH = bp.get_test_path()


def load_data(path) -> List[Tuple[int]]:
    with open(path, "r") as f:
        input_ = f.read().splitlines()
    out = []

    for line in input_:
        points = line.split(" -> ")
        out.append([tuple(map(int, point.split(","))) for point in points])

    return out


def filter_(data: List[List[int]]) -> List[List[int]]:
    """Filter out lines that are not horizontal or vertical"""
    out = []
    for line in data:
        if line[0][0] == line[1][0] or line[0][1] == line[1][1]:
            out.append(line)

    return out


def make_line(row) -> Set[Tuple[int]]:
    x1, y1 = row[0]
    x2, y2 = row[1]

    xstep = ystep = 1
    if y1 > y2:
        ystep = -1
    if x1 > x2:
        xstep = -1

    if x1 == x2:
        # Vertical line
        return {(x1, y) for y in range(y1, y2 + ystep, ystep)}
    if y1 == y2:
        # Horizontal line
        return {(x, y1) for x in range(x1, x2 + xstep, xstep)}

    # Diagonal line
    return {(x, y)
            for x, y in zip(range(x1, x2 +
                                  xstep, xstep), range(y1, y2 + ystep, ystep))}


def make_lines(data: int):
    """Make a list of lines from the data"""
    lines = set()
    seen = set()
    for row in data:
        row_line = make_line(row)
        row_seen = row_line & lines
        lines |= row_line
        seen |= row_seen

    out = len(seen)

    return out


def main():
    start = time.time()
    test = load_data(TEST_PATH)
    test_lines = make_lines(test)
    assert test_lines == 12

    data = load_data(DATA_PATH)
    lines = make_lines(data)
    print(lines)


if __name__ == "__main__":
    main()
