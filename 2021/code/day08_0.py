"""https://adventofcode.com/2021/day/8"""
import itertools
import os
from typing import List

import boilerplate as bp

DATA_PATH = os.path.join(bp.data_dir, "day08.txt")
TEST_PATH = os.path.join(bp.test_dir, "day08.txt")

def load_data(path):
    with open(path) as f:
        data = f.read().splitlines()
    intermediate = [line.split(" | ")[1] for line in data]
    out = itertools.chain.from_iterable(map(lambda x: x.split(), intermediate))
    return out


def count_numbers(data: List[str]):
    out = [0] * 10
    for d in data:
        match len(d):
            case 2:
                out[1] += 1
            case 4:
                out[4] += 1
            case 3:
                out[7] += 1
            case 7:
                out[8] += 1
    return sum(out)

def test():
    data = load_data(TEST_PATH)
    assert count_numbers(data) == 26

if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(count_numbers(data))
