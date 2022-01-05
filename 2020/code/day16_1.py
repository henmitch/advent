"""https://adventofcode.com/2020/day/16"""
import functools
import operator
from typing import Tuple

from day16_0 import (DATA_PATH, Rules, Ticket, Tickets,
                     invalid_numbers_in_ticket, load_data)


def is_valid(ticket: Ticket, rules: Rules) -> bool:
    return not invalid_numbers_in_ticket(ticket, rules)


def get_valid_tickets(tickets: Tickets, rules: Rules) -> Tickets:
    return tuple(filter(lambda x: is_valid(x, rules), tickets))


def associate(tickets: Tickets, rules: Rules) -> Tuple[str, ...]:
    tickets = get_valid_tickets(tickets, rules)
    l = len(tickets[0])
    associations = {name: set(i for i in range(l)) for name, _ in rules}
    while any(len(association) > 1 for association in associations.values()):
        for ticket in tickets:
            for idx, number in enumerate(ticket):
                for name, (low, high) in rules:
                    if number not in low and number not in high:
                        associations[name] -= {idx}
                        break
        for name, idxes in associations.items():
            if len(idxes) == 1:
                for other in associations:
                    if other == name:
                        continue
                    associations[other] -= idxes

    out = ["" for _ in range(l)]
    for association, num in associations.items():
        out[max(num)] = association

    return tuple(out)


def departure_product(rules: Rules, ticket: Ticket, tickets: Tickets) -> int:
    associations = associate(tickets, rules)
    departure_idxes = [
        i for i, name in enumerate(associations) if "departure" in name
    ]
    return functools.reduce(operator.mul, (ticket[i] for i in departure_idxes))


if __name__ == "__main__":
    data = load_data(DATA_PATH)
    print(departure_product(*data))
