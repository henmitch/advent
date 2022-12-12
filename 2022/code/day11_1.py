"""https://adventofcode.com/2022/day/11"""
from functools import reduce
from operator import mul

from day11_0 import DATA_PATH, TEST_PATH, Monkey


def round(monkeys: list[Monkey], max_: int = 0) -> list[Monkey]:
    for monkey in monkeys:
        for to, item in monkey.turn():
            if max_ and item > max_:
                item = item%max_
            monkeys[to].holding.append(item)
    return monkeys


def run(monkeys: list[Monkey], n: int = 20) -> int:
    max_ = reduce(mul, (monkey.check_by for monkey in monkeys))
    for _ in range(n):
        monkeys = round(monkeys, max_)
    viewings = sorted(monkey.total_inspections for monkey in monkeys)
    return viewings[-1]*viewings[-2]


def load_data(path: str) -> list[Monkey]:
    with open(path, "r") as f:
        raw = f.read().split("\n\n")
    return [Monkey(data, 1) for data in raw]


def test():
    data = load_data(TEST_PATH)
    assert run(data, 10_000) == 2713310158


def main():
    data = load_data(DATA_PATH)
    print(run(data, 10_000))


if __name__ == "__main__":
    test()
    main()
