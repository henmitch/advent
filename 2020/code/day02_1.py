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
        (idx1, idx2) = map(int, counts.split("-"))
        letter = letter[0]
        out.append(((idx1, idx2), letter, password))

    return out


def valid(line):
    (idx1, idx2), letter, password = line
    return (password[idx1 - 1] == letter) ^ (password[idx2 - 1] == letter)


def count_valid(lines):
    return sum(valid(line) for line in lines)


def test():
    data = load_data(TEST_PATH)
    assert count_valid(data) == 1


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(count_valid(data))
