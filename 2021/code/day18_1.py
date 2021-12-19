"""https://adventofcode.com/2021/day/18"""
import itertools
from typing import List
import ast
from day18_0 import DATA_PATH, TEST_PATH, SnailfishNumber


def load_data(path) -> List:
    with open(path, "r") as f:
        data = f.read().splitlines()
    return [ast.literal_eval(line) for line in data]


def max_sum(data: List) -> int:
    out = 0
    for first, second in itertools.combinations(data, 2):
        first = SnailfishNumber(first)
        second = SnailfishNumber(second)
        out = max(out, (first + second).magnitude())
    return out

if __name__ == "__main__":
    data = load_data(DATA_PATH)
    print(max_sum(data))
