"""https://adventofcode.com/2019/day/4"""
from day04_0 import Pair, increasing, make_range, repeating, split_into_pairs
from collections import Counter


def valid(val: int) -> bool:
    val_str = str(val)

    val = split_into_pairs(val)

    for pair in val:
        if not increasing(pair):
            return False

    counteds = Counter(Counter(val_str).values())

    return counteds[2] > 0


def count_in_range(vals: range) -> int:
    return sum(valid(val) for val in vals)


def run(vals: str) -> int:
    return count_in_range(make_range(vals))


def test():
    assert valid(223456)
    assert valid(111122)
    assert valid(444566)
    assert not valid(444567)
    assert not valid(123444)
    assert not valid(223450)
    assert not valid(123789)


def main():
    print(run("254032-789860"))


if __name__ == "__main__":
    test()
    main()
