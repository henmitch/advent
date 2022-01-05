"""https://adventofcode.com/2020/day/16"""
from typing import Tuple
import boilerplate as bp

Ticket = Tuple[int, ...]
Tickets = Tuple[Ticket, ...]
Rule = Tuple[str, Tuple[range, range]]
Rules = Tuple[Rule, ...]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> Tuple[Rules, Ticket, Tickets]:
    with open(path, "r") as f:
        raw_rules, raw_mine, raw_nearby = f.read().split("\n\n")
    rules = []
    for row in raw_rules.splitlines():
        name, ranges = row.split(": ")
        low, high = _str_to_ranges(ranges)
        rules.append((name, (low, high)))

    mine = parse_ticket(raw_mine.split("\n")[1])

    nearby = []
    for row in raw_nearby.splitlines()[1:]:
        nearby.append(parse_ticket(row))

    return tuple(rules), mine, tuple(nearby)


def _str_to_range(s: str) -> range:
    low, high = s.split("-")
    return range(int(low), int(high) + 1)


def _str_to_ranges(s: str) -> Tuple[range, range]:
    return tuple(_str_to_range(r) for r in s.split(" or "))


def parse_ticket(s: str) -> Ticket:
    return tuple(int(i) for i in s.split(","))


def invalid_numbers_in_ticket(ticket: Ticket, rules: Rules) -> Tuple[int]:
    out = []
    for number in ticket:
        for _, (low, high) in rules:
            if number in low or number in high:
                break
        else:
            out.append(number)
    return tuple(out)


def invalid_numbers_in_tickets(tickets: Tickets, rules: Rules) -> Tuple[int]:
    out = []
    for ticket in tickets:
        out.extend(invalid_numbers_in_ticket(ticket, rules))
    return tuple(out)


def run(rules: Rules, _: Ticket, nearby: Tickets) -> int:
    return sum(invalid_numbers_in_tickets(nearby, rules))


def test():
    data = load_data(TEST_PATH)
    assert run(*data) == 71


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(run(*data))
