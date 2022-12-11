"""https://adventofcode.com/2022/day/11"""
from collections.abc import Iterator
import re
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def first_number(line: str):
    return int(re.findall(r"(\d+)", line)[0])


class Monkey:

    def __init__(self, data: str, divide_by: int = 3) -> None:
        num, start, op, check, t, f = data.splitlines()
        self.num = first_number(num)
        self.holding: list[int] = list(map(int, re.findall(r"(\d+)", start)))

        self.by = op.split()[-1]
        self.operation_name: str = re.findall(r"([\+\*])", op)[0]

        self.check_by = first_number(check)
        self.if_t = first_number(t)
        self.if_f = first_number(f)

        self.total_inspections = 0
        self.divide_by = divide_by

    def op(self, num) -> int:
        if self.by == "old":
            by = num
        else:
            by = int(self.by)
        if self.operation_name == "+":
            return num + by
        elif self.operation_name == "*":
            return num*by
        else:
            raise ValueError("Operation was neither '+' nor '*'")

    def check(self, n: int) -> int:
        if n%self.check_by:
            return self.if_f
        return self.if_t

    def turn(self) -> Iterator[tuple[int, int]]:
        while self.holding:
            num = self.op(self.holding.pop(0))//self.divide_by
            self.total_inspections += 1
            yield self.check(num), num


def round(monkeys: list[Monkey]) -> list[Monkey]:
    for monkey in monkeys:
        for to, item in monkey.turn():
            monkeys[to].holding.append(item)
    return monkeys


def run(monkeys: list[Monkey], n: int = 20) -> int:
    for i in range(n):
        monkeys = round(monkeys)
        if not (i + 1) % 500:
            print(f"{i + 1}/{n}")
    viewings = sorted(monkey.total_inspections for monkey in monkeys)
    return viewings[-1]*viewings[-2]


def load_data(path: str) -> list[Monkey]:
    with open(path, "r") as f:
        raw = f.read().split("\n\n")
    return [Monkey(data) for data in raw]


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 10605


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
