"""https://adventofcode.com/2020/day/18"""
from __future__ import annotations
import operator
from typing import List
from day18_0 import load_data, DATA_PATH


def parse(line: str) -> int:
    while "(" in line:
        for i, val in enumerate(line):
            if line[i] == "(":
                sub_line = extract(line[i:])
                idx = min(len(sub_line) + 3 + i, len(line) - 1)

                if line[idx] in ["+", "*"]:
                    op = f" {line[idx]} "
                    idx += 2
                else:
                    op = " "
                # line = parse(f"{parse(sub_line)}{op}{line[idx:]}")
                line = f"{line[:i]} {parse(sub_line)}{op}{line[idx:]}"
                break

    try:
        int(line)
        return line
    except ValueError:
        pass

    while True:
        line = line.split()
        new_line = []
        for i, val in enumerate(line):
            if val[0] == "(":
                new_line.append(parse(" ".join(line[i:])))
                line = " ".join(new_line)
                break
            if line[i - 1] == "+":
                new_line.pop()
                new_line.append(int(new_line.pop()) + int(val))
            else:
                new_line.append(val)
        else:
            break

    line = new_line
    new_line = []
    for i, val in enumerate(line):
        if line[i - 1] == "*":
            new_line.pop()
            new_line.append(int(new_line.pop())*int(val))
        else:
            new_line.append(val)

    return int(new_line[0])


def extract(line: str) -> str:
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
    return sub_line[:-1]


def run(lines: List[str]) -> int:
    return sum(parse(line) for line in lines)


def test():
    assert parse("1 + 2 * 3 + 4 * 5 + 6") == 231
    assert parse("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert parse("2 * 3 + (4 * 5)") == 46
    assert parse("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
    assert parse("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
    assert parse("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(run(data))
