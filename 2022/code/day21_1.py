"""https://adventofcode.com/2022/day/21"""
from __future__ import annotations

import re
from numbers import Number
from operator import __eq__, add, truediv, mul, sub
from typing import Callable, Any

from day21_0 import DATA_PATH, OPS, TEST_PATH

OPPOSITES = {add: sub, sub: add, mul: truediv, truediv: mul}


def load_data(path: str) -> dict[str, str]:
    with open(path, "r") as f:
        raw = f.read().replace(" ", "").splitlines()
    return dict(line.split(":") for line in raw)


def make_int_if_possible(s: str) -> int | str:
    if isinstance(s, str) and s.isnumeric():
        return int(s)
    return s


class Operation:

    def __init__(self, op: Callable, n1: str | int | Operation,
                 n2: str | int | Operation) -> None:
        self.op = op
        self.values = tuple(make_int_if_possible(n) for n in (n1, n2))

    def __str__(self) -> str:
        return f"{self.op}({', '.join(str(v) for v in self.values)})"

    def __repr__(self) -> str:
        return str(self)

    def __contains__(self, val: Any) -> bool:
        if any(n == val for n in self.values):
            return True
        for n in self.values:
            if isinstance(n, Operation) and val in n:
                return True
        return False

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Operation):
            return False
        return self.op == __value.op and self.values == __value.values

    def inverse(self) -> Callable:
        n1, n2 = self.values
        if isinstance(n1, Operation):
            n1 = n1.collapse()
        if isinstance(n2, Operation):
            n2 = n2.collapse()
        if isinstance(n1, str) or (isinstance(n1, Operation)
                                   and n1.contains_variable()):
            return n1, lambda x: OPPOSITES[OPS[self.op]](x, n2)
        if isinstance(n2, str) or (isinstance(n2, Operation)
                                   and n2.contains_variable()):
            # Special case: need to subtract the variable
            # n1 - f(humn) = x ==> f(humn) = n1 - x
            if self.op == "-":
                return n2, lambda x: n1 - x
            return n2, lambda x: OPPOSITES[OPS[self.op]](x, n1)

    def contains_variable(self) -> bool:
        if any(isinstance(n, str) for n in self.values):
            return True
        if all(isinstance(n, Number) for n in self.values):
            return False
        for n in self.values:
            if isinstance(n, Operation) and n.contains_variable():
                return True
        return False

    def collapse(self) -> Operation | int:
        newer_operation = Operation(self.op, *self.values)
        new_operation = None
        # Collapsing until we can't anymore
        while new_operation != newer_operation:
            new_operation = newer_operation
            newer_values = []
            for n in newer_operation.values:
                if isinstance(n, Operation):
                    new_n = n.collapse()
                else:
                    new_n = n
                newer_values.append(new_n)
            newer_operation = Operation(self.op, *newer_values)
        if all(isinstance(n, Number) for n in newer_operation.values):
            out = OPS[newer_operation.op](*newer_operation.values)
            return out
        return newer_operation

    def substitute(self, variable: str, value: int) -> None:
        n1, n2 = self.values
        if n1 == variable:
            n1 = value
        if n2 == variable:
            n2 = value
        if isinstance(n1, Operation):
            n1.substitute(variable, value)
        if isinstance(n2, Operation):
            n2.substitute(variable, value)
        self.values = n1, n2


def extract(s: str) -> tuple[str, str, str] | str:
    extracted = re.match(r"(\w+) ?([\+=\/\-\*]) ?(\w+)", s)
    if extracted is None:
        return s
    return extracted.groups()


def get_equation(data: dict[str, str]) -> dict[str, str | Number | Operation]:
    out = data.copy()
    out["humn"] = "humn"
    out["root"] = out["root"].replace("+", "=")
    # Get our numbers set first, for simplicity's sake
    for k, v in out.items():
        new_v = make_int_if_possible(v)
        # Do nothing if we're looking at "humn" or a number
        if not isinstance(new_v, str) or new_v == "humn":
            out[k] = new_v
            continue
        # Convert everybody else to an Operation
        n1, op, n2 = extract(new_v)
        out[k] = Operation(op, n1, n2)
    # Substitute operations in
    for k, v in out.items():
        # Can only substitute into operations
        if not isinstance(v, Operation):
            continue
        for n in v.values:
            if n in out:
                v.substitute(n, out[n])
    return out


def find_answer(data: dict[str, Operation | int]) -> int:
    root = data["root"]
    lhs, rhs = root.values
    rhs = rhs.collapse()
    while "humn" not in [lhs, rhs]:
        new_lhs, inv = lhs.inverse()
        lhs, rhs = new_lhs, inv(rhs)
    return ({lhs, rhs} - {"humn"}).pop()


def run(data: dict[str, str]) -> int:
    return find_answer(get_equation(data))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 301


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
