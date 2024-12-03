"""https://adventofcode.com/2024/day/3"""
import re

import boilerplate as bp

Pair = tuple[int, int]

TEST_PATH = bp.get_test_path("0")
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[Pair]:
    with open(path, "r") as f:
        raw = f.read()
    return parse(raw)


def parse(line: str) -> list[Pair]:
    muls = re.findall(r"mul\((\d{0,3}),(\d{0,3})\)", line)
    return [(int(a), int(b)) for a, b in muls]


def run(data: list[Pair]) -> int:
    return sum(a*b for a, b in data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 161


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
