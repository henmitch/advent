"""https://adventofcode.com/2022/day/21"""
from numbers import Number
from operator import add, mul, sub, truediv, __eq__
from typing import Callable

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

OPS = {"+": add, "*": mul, "-": sub, "/": truediv}


def load_data(path: str) -> dict[str, str]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return dict(line.split(": ") for line in raw)


def operate(s: str) -> tuple[Callable, str, str]:
    first, op, second = s.split(" ")
    return OPS[op], first, second


def parse(data: dict[str, str]) -> dict[str, Number]:
    out = data.copy()
    while not isinstance(out["root"], Number):
        for k, v in out.items():
            if isinstance(v, Number):
                continue
            if v.isnumeric():
                out[k] = int(v)
                continue
            op, n1, n2 = operate(v)
            if isinstance(out[n1], Number) and isinstance(out[n2], Number):
                out[k] = op(out[n1], out[n2])
    return out


def run(data: dict[str, str]) -> int:
    return int(parse(data)["root"])


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 152


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
