"""https://adventofcode.com/2020/day/4"""
import os
from typing import List

import boilerplate as bp

DATA_PATH = os.path.join(bp.data_dir, "day04.txt")
TEST_PATH = os.path.join(bp.test_dir, "day04.txt")

EXPECTED_KEYS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]


def load_data(path):
    with open(path) as f:
        raw = f.read()
    return raw.split("\n\n")


def parse(passport: str) -> dict:
    out = {}
    for line in passport.split():
        k, v = line.split(":")
        out[k] = v
    return out


def valid(passport: dict) -> bool:
    return all(k in passport for k in EXPECTED_KEYS)


def valid_count(data: List[str]) -> int:
    return sum(valid(parse(p)) for p in data)


def test():
    data = load_data(TEST_PATH)
    assert valid_count(data) == 2


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(valid_count(data))
