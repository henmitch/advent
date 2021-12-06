"""You come across a field of hydrothermal vents on the ocean floor! These
vents constantly produce large, opaque clouds, so it would be best to avoid
them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby
lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
Each line of vents is given as a line segment in the format x1,y1 -> x2,y2
where x1,y1 are the coordinates of one end the line segment and x2,y2 are the
coordinates of the other end. These line segments include the points at both
ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
For now, only consider horizontal and vertical lines: lines where either
x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the
following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9.
Each position is shown as the number of lines which cover that point or . if no
line covers that point. The top-left pair of 1s, for example, comes from
2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9
and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points
where at least two lines overlap. In the above example, this is anywhere in the
diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two
lines overlap?
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
        return [(x1, y) for y in range(y1, y2 + 1)]
    if y1 == y2:
        # Horizontal line
        if x1 > x2:
            x1, x2 = x2, x1
        return [(x, y1) for x in range(x1, x2 + 1)]


def make_lines(data: List[List[int]]):
    """Make a list of lines from the data"""
    logging.info("Making lines")
    out = []
    for row in data:
        out += make_line(row)

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
    test_lines = make_lines(test)
    test_overlap = count_overlap(test_lines)
    assert test_overlap == 5
    logging.info("Test passed")

    data = filter_(load_data(DATA_PATH))
    lines = make_lines(data)
    print(count_overlap(lines))


if __name__ == "__main__":
    logging.info("Main")
    main()
