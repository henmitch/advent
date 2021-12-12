"""https://adventofcode.com/2020/day/2"""
import os

import boilerplate as bp

DATA_PATH = os.path.join(bp.data_dir, "day02.txt")
TEST_PATH = os.path.join(bp.test_dir, "day02.txt")


def load_data(path):
    with open(path) as f:
        lines = f.read().splitlines()
    out = []
    for line in lines:
        counts, letter, password = line.split()
        (min_count, max_count) = map(int, counts.split("-"))
        letter = letter[0]
        out.append(((min_count, max_count), letter, password))

    return out


def valid(line):
    (min_count, max_count), letter, password = line
    count = password.count(letter)
    return min_count <= count <= max_count


def count_valid(lines):
    return sum(valid(line) for line in lines)


def test():
    data = load_data(TEST_PATH)
    assert count_valid(data) == 2


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(count_valid(data))
