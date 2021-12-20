"""https://adventofcode.com/2021/day/5"""
import logging
import time
from typing import List

import boilerplate as bp

logging.basicConfig(level=logging.WARN)

DATA_PATH = bp.get_data_path()
TEST_PATH = bp.get_test_path()


def load_data(path):
    logging.info(f"Loading data from {path}")
    with open(path, "r") as f:
        input_ = f.read().splitlines()
    out = []

    for line in input_:
        points = line.split(" -> ")
        out.append([tuple(map(int, point.split(","))) for point in points])

    return out


def filter_(data: List[List[int]]):
    """Filter out lines that are not horizontal or vertical"""
    logging.info("Filtering data")
    out = []
    for line in data:
        if line[0][0] == line[1][0] or line[0][1] == line[1][1]:
            out.append(line)

    return out


def make_line(row):
    logging.info(f"Making line {row}")
    x1, y1 = row[0]
    x2, y2 = row[1]
    if x1 == x2:
        # Vertical line
        if y1 > y2:
            y1, y2 = y2, y1
        return {(x1, y) for y in range(y1, y2 + 1)}
    if y1 == y2:
        # Horizontal line
        if x1 > x2:
            x1, x2 = x2, x1
        return {(x, y1) for x in range(x1, x2 + 1)}


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


def find_overlap(points: List[List[int]]):
    """Find the points where two lines overlap"""
    logging.info("Finding overlap")
    out = set()
    for point in set(points):
        if points.count(point) > 1:
            out |= {point}

    return list(out)


def count_overlap(points: List[List[int]]):
    """Count the number of points where two lines overlap"""
    logging.info("Counting overlap")
    return len(find_overlap(points))


def main():
    logging.info(time.time())
    logging.info("Starting")
    test = filter_(load_data(TEST_PATH))
    test_overlap = make_lines(test)
    assert test_overlap == 5
    logging.info("Test passed")

    data = filter_(load_data(DATA_PATH))
    print(make_lines(data))


if __name__ == "__main__":
    logging.info("Main")
    main()
