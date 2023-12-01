"""https://adventofcode.com/2023/day/1"""
import re

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def process(line: str) -> int:
    digits = re.findall(r"\d", line)
    return int(digits[0])*10 + int(digits[-1])


def run(data: list[str]) -> int:
    return sum(map(process, data))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 142


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
