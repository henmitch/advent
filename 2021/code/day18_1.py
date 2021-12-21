"""https://adventofcode.com/2021/day/18"""
import ast
import itertools
from typing import List

from day18_0 import DATA_PATH, SnailfishNumber


def load_data(path) -> List[SnailfishNumber]:
    with open(path, "r") as f:
        data = f.read().splitlines()
    return tuple(ast.literal_eval(line) for line in data)


def max_sum(data: List[SnailfishNumber]) -> int:
    return max(
        SnailfishNumber(pair).reduce().magnitude()
        for pair in itertools.permutations(data, 2))


if __name__ == "__main__":
    data = load_data(DATA_PATH)
    print(max_sum(data))
