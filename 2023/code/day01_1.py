"""https://adventofcode.com/2023/day/1"""
import re

import boilerplate as bp

TEST_PATH = bp.get_test_path("1")
DATA_PATH = bp.get_data_path()

mappings = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def load_data(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def process(line: str) -> int:
    # Capture group in a lookahead to allow for overlapping matches
    digits = re.findall(r"(?=(\d|" + "|".join(mappings.keys()) + "))", line)
    digits = [mappings.get(digit, digit) for digit in digits]
    return int(digits[0])*10 + int(digits[-1])


def run(data: list[str]) -> int:
    return sum(map(process, data))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 281


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
