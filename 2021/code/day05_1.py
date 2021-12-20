"""https://adventofcode.com/2021/day/5"""
import logging
import time
from typing import List

import boilerplate as bp

logging.basicConfig(level=logging.WARN)

DATA_PATH = bp.get_data_path()
TEST_PATH = bp.get_test_path()


def load_data(path) -> List[List[int]]:
    logging.info(f"Loading data from {path}")
    with open(path, "r") as f:
        input_ = f.read().splitlines()
    out = []

    for line in input_:
        points = line.split(" -> ")
        out.append([tuple(map(int, point.split(","))) for point in points])

    return out


def filter_(data: List[List[int]]) -> List[List[int]]:
    """Filter out lines that are not horizontal or vertical"""
    logging.info("Filtering data")
    out = []
    for line in data:
        if line[0][0] == line[1][0] or line[0][1] == line[1][1]:
            out.append(line)

    return out


def make_line(row) -> List[List[int]]:
    logging.debug(f"Making line {row}")
    x1, y1 = row[0]
    x2, y2 = row[1]

    xstep = ystep = 1
    if y1 > y2:
        ystep = -1
    if x1 > x2:
        xstep = -1

    if x1 == x2:
        # Vertical line
        return [(x1, y) for y in range(y1, y2 + ystep, ystep)]
    if y1 == y2:
        # Horizontal line
        return [(x, y1) for x in range(x1, x2 + xstep, xstep)]

    # Diagonal line
    return [(x, y)
            for x, y in zip(range(x1, x2 +
                                  xstep, xstep), range(y1, y2 + ystep, ystep))]


def make_lines(data: List[List[int]]):
    """Make a list of lines from the data"""
    logging.info("Making lines")
    lines = set()
    seen = set()
    out = 0
    for row in data:
        row_line = make_line(row)
        row_seen = set(row_line) & lines - seen
        out += len(row_seen)
        lines |= set(row_line)
        seen |= row_seen

    return out


def main():
    start = time.time()
    logging.info("Starting")
    test = load_data(TEST_PATH)
    test_lines = make_lines(test)
    assert test_lines == 12
    logging.info("Test passed")

    data = load_data(DATA_PATH)
    lines = make_lines(data)
    print(lines)
    logging.info(f"Finished in {time.time() - start:.2f} seconds")


if __name__ == "__main__":
    logging.info("Main")
    main()
