"""https://adventofcode.com/2022/day/13"""
import ast
from functools import cmp_to_key

from day13_0 import DATA_PATH, TEST_PATH, Packet, compare


def load_data(path: str) -> list[Packet]:
    with open(path, "r") as f:
        raw = set(f.read().splitlines()) - {""}
    return [ast.literal_eval(line) for line in raw] + [[[2]], [[6]]]


def compare_as_num(left: Packet, right: Packet) -> int:
    if (c := compare(left, right)) is None:
        return 0
    return 2*int(c) - 1


def sort(data: list[Packet]) -> list[Packet]:
    return sorted(data, key=cmp_to_key(compare_as_num), reverse=True)


def run(data: list[Packet]) -> int:
    s = sort(data)
    return (1 + s.index([[2]]))*(1 + s.index([[6]]))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 140


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
