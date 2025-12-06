"""https://adventofcode.com/2025/day/6"""
import re

import boilerplate as bp
from day06_0 import DATA_PATH, TEST_PATH, run


def load_data(path: str) -> tuple[list[list[int]], list[str]]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    nums_r, ops_r = raw[:-1], raw[-1]
    max_line_length = max(len(line) for line in nums_r)
    nums_r = [line.ljust(max_line_length) for line in nums_r]
    # cols = ["".join(line).replace(" ", "0") for line in zip(*nums_r)]
    cols = ["".join(line) for line in zip(*nums_r)]
    nums = []
    while cols:
        group = []
        while cols and (num := cols.pop(0)):
            if set(num) == {" "}:
                break
            group.append(int(num))
        nums.append(group)
    ops = re.findall(r"[*+]", ops_r)
    return nums, ops


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 3263827


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
