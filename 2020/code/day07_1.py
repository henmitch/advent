"""https://adventofcode.com/2020/day/7"""
from typing import Dict
import day07_0 as old


def count_children(target: str, bags: Dict[str, Dict[str, int]]) -> int:
    out = 0
    for bag, n in bags[target].items():
        out += (1 + count_children(bag, bags))*n

    return out


def test():
    data = old.load_data(old.TEST_PATH)
    assert count_children("shiny gold", data) == 32


if __name__ == "__main__":
    test()
    data = old.load_data(old.DATA_PATH)
    print(count_children("shiny gold", data))
