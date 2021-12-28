"""https://adventofcode.com/2020/day/7"""
import re
from typing import Dict, Set

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> Dict[str, Dict[str, int]]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    out = {}
    for line in raw:
        split = line.split(" bags contain ")
        out[split[0]] = {}
        if split[1] == "no other bags.":
            continue
        bags = split[1].split(", ")
        for bag in bags:
            match = re.match(r"(\d+) ([\w ]+) bag", bag)
            out[split[0]][match.group(2)] = int(match.group(1))
    return out


def holders(target: str, bags: Dict[str, Dict[str, int]]) -> Set[str]:
    out = set()
    for bag, contents in bags.items():
        if target in contents:
            out |= {bag} | holders(bag, bags)
    return out


def count(target: str, bags: Dict[str, Dict[str, int]]) -> int:
    return len(holders(target, bags))


def test():
    data = load_data(TEST_PATH)
    assert count("shiny gold", data) == 4


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(count("shiny gold", data))
