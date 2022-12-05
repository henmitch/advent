"""https://adventofcode.com/2022/day/3"""
from functools import reduce
from operator import and_
from day03_0 import load_data, TEST_PATH, DATA_PATH, priority


def identify_badge(trio: list[str]) -> str:
    return reduce(and_, (set(sack) for sack in trio)).pop()


def find_all_badges(data: list[str]) -> list[str]:
    return [identify_badge(data[i:i + 3]) for i in range(0, len(data), 3)]


def badge_priorities(data: list[str]) -> int:
    return sum(priority(badge) for badge in find_all_badges(data))


def test():
    data = load_data(TEST_PATH)
    assert badge_priorities(data) == 70


def main():
    data = load_data(DATA_PATH)
    print(badge_priorities(data))


if __name__ == "__main__":
    test()
    main()
