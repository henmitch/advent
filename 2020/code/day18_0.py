"""https://adventofcode.com/2020/day/18"""
import operator
from typing import Tuple
import boilerplate as bp

DATA_PATH = bp.get_data_path()


def load_data(path: str) -> Tuple[str]:
    with open(path, "r") as f:
        return tuple(f.read().splitlines())


def parse(line: str) -> int:
    if line[0] == "(":
        so_far, idx = stackify(line)
    else:
        so_far = int(line[0])
        idx = 1

    op = None
    line = line[idx:]
    while line:
        char = line[0]
        if char == " ":
            idx = 1
        elif char == "+":
            op = operator.add
            idx = 1
        elif char == "*":
            op = operator.mul
            idx = 1
        elif char == "(":
            next_num, idx = stackify(line)
            so_far = op(so_far, next_num)
        else:
            so_far = op(so_far, int(char))
            idx = 1
        line = line[idx:]

    return so_far


def stackify(line):
    sub_line = ""
    stack = 1
    line_iter = iter(line[1:])
    while stack:
        char = next(line_iter)
        if char == "(":
            stack += 1
        if char == ")":
            stack -= 1
        sub_line += char
    so_far = parse(sub_line[:-1])
    idx = len(sub_line) + 2
    return so_far, idx


def run(lines: Tuple[str]) -> int:
    return sum(parse(line) for line in lines)


def test():
    assert parse("1 + 2 * 3 + 4 * 5 + 6") == 71
    assert parse("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert parse("2 * 3 + (4 * 5)") == 26
    assert parse("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
    assert parse("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
    assert parse("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(run(data))
