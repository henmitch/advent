"""https://adventofcode.com/2025/day/6"""
import re
from operator import add, mul
from functools import reduce
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

OPS = {"+": add, "*": mul}


def load_data(path: str) -> tuple[list[list[int]], list[str]]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    nums_r, ops_r = raw[:-1], raw[-1]
    nums = list(zip(*(map(int, re.findall(r"\d+", line)) for line in nums_r)))
    ops = re.findall(r"[*+]", ops_r)
    return nums, ops


def run(data: tuple[list[list[int]], list[str]]) -> int:
    out = 0
    for nums, op in zip(*data):
        out += reduce(OPS[op], nums)
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 4277556


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
