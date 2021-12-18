"""https://adventofcode.com/2021/day/10"""
import re
from typing import List

import boilerplate as bp

DATA_PATH = bp.get_data_path()
TEST_PATH = bp.get_test_path()

VALID_PAIRS = re.compile(r"(?:\(\)|\{\}|\[\]|<>)")
OPENERS = {"(", "{", "[", "<"}
CLOSERS = {")", "}", "]", ">"}


def load_data(path):
    """Load data from file"""
    with open(path, "r") as f:
        return f.read().splitlines()


def remove_valid(line: str) -> str:
    """Recursively remove all valid values from line"""
    if re.search(VALID_PAIRS, line):
        return remove_valid(re.sub(VALID_PAIRS, "", line))
    return line


def find_invalid_char(line: str) -> str:
    cleaned = remove_valid(line)
    for char in cleaned:
        if char in CLOSERS:
            return char
    return ""


def find_all_invalid_chars(data: List[str]) -> List[str]:
    """Find all invalid characters in data"""
    return [find_invalid_char(line) for line in data]


def score_invalid(data: List[str]) -> int:
    """Score invalid characters"""
    scores = {"": 0, ")": 3, "]": 57, "}": 1197, ">": 25137}
    return sum(scores[char] for char in find_all_invalid_chars(data))


def test():
    data = load_data(TEST_PATH)
    assert score_invalid(data) == 26397


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(score_invalid(data))
