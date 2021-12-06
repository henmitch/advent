"""Unfortunately, considering only horizontal and vertical lines doesn't give
you the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in
your list will only ever be horizontal, vertical, or a diagonal line at exactly
45 degrees. In other words:

An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
Considering all lines from the above example would now produce the following
diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
You still need to determine the number of points where at least two lines
overlap. In the above example, this is still anywhere in the diagram with a 2
or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?
"""
import logging
import os
import time
from typing import List

logging.basicConfig(level=logging.INFO)

data_dir = os.path.join(os.path.dirname(__file__), "data")
test_dir = os.path.join(os.path.dirname(__file__), "test")
DATA_PATH = os.path.join(data_dir, "day05_0.txt")
TEST_PATH = os.path.join(test_dir, "day05_0.txt")


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
