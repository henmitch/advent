"""https://adventofcode.com/2023/day/19"""
from __future__ import annotations

import copy
from collections import deque
from dataclasses import astuple, dataclass
from functools import reduce
from operator import or_

from day19_0 import DATA_PATH, TEST_PATH, Rule, Workflow

Workflows = dict[str, Workflow]
Pair = tuple[int, int]


@dataclass
class GenericPart:
    x: Pair
    m: Pair
    a: Pair
    s: Pair

    def __init__(
        self,
        x: Pair = (1, 4000),
        m: Pair = (1, 4000),
        a: Pair = (1, 4000),
        s: Pair = (1, 4000)
    ) -> None:
        self.x, self.m, self.a, self.s = x, m, a, s

    def apply(self,
              rule: Rule) -> tuple[GenericPart | None, GenericPart | None]:
        if rule.comparison is None:
            return self, None
        min_, max_ = getattr(self, rule.category)
        passes, fails = copy.copy(self), copy.copy(self)
        if rule.comparison == ">":
            if min_ > rule.target:
                return self, None
            if max_ <= rule.target:
                return None, self
            setattr(passes, rule.category, (rule.target + 1, max_))
            setattr(fails, rule.category, (min_, rule.target))
        elif rule.comparison == "<":
            if max_ < rule.target:
                return self, None
            if min_ >= rule.target:
                return None, self
            setattr(passes, rule.category, (min_, rule.target - 1))
            setattr(fails, rule.category, (rule.target, max_))
        else:
            raise RuntimeError(f"Invalid rule {rule} applied to {self}")
        return passes, fails

    def n_parts(self) -> int:
        out = 1
        for min_, max_ in astuple(self):
            if min_ == max_:
                return 0
            out *= max_ - min_ + 1
        return out


def load_data(path: str) -> dict[str, Workflow]:
    with open(path, "r") as f:
        workflows, _ = f.read().split("\n\n")
    workflows = reduce(or_, (_parse_workflow(line)
                             for line in workflows.splitlines()))
    return workflows


def _parse_workflow(line: str) -> dict[str, Workflow]:
    name, raw = line.split("{")
    raw_rules = raw[:-1].split(",")
    rules = [Rule(rule) for rule in raw_rules]
    return {name: Workflow(rules)}


def overlap(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] <= b[0] <= a[1] or a[0] <= b[1] <= a[1]


def run(data: Workflows) -> int:
    to_apply = deque([("in", GenericPart())])
    out: list[GenericPart] = []
    while to_apply:
        name, fails = to_apply.popleft()
        if name == "A":
            out.append(fails)
            continue
        if name == "R":
            continue
        for rule in data[name].rules:
            passes, fails = fails.apply(rule)
            if passes is not None:
                to_apply.append((rule.output, passes))
            if fails is None:
                break
    return sum(part.n_parts() for part in out)


def test():
    data = load_data(TEST_PATH)
    expect = 167_409_079_868_000
    out = run(data)
    assert out == expect


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
