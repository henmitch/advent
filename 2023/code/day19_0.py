"""https://adventofcode.com/2023/day/19"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import reduce
from operator import or_

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def total(self) -> int:
        return self.x + self.m + self.a + self.s

    def __getitem__(self, key: str) -> int:
        return asdict(self)[key]


class Rule:

    def __init__(self, rule: str) -> None:
        self.rule = rule
        if ":" not in rule:
            self.comparison = None
            self.output = rule
            return
        question, output = rule.split(":")
        self.category = question[0]
        self.comparison = question[1]
        self.target = int(question[2:])
        self.output = output

    def __call__(self, part: Part) -> str | None:
        if self.comparison is None:
            return self.output
        if self.comparison == ">":
            if part[self.category] > self.target:
                return self.output
        elif self.comparison == "<":
            if part[self.category] < self.target:
                return self.output
        return None

    def __repr__(self) -> str:
        return self.rule

    def inverse(self) -> Rule:
        if self.comparison is None:
            return self
        if self.comparison == ">":
            return Rule(f"{self.category}<{self.target+1}:_")
        return Rule(f"{self.category}>{self.target-1}:_")


class Workflow:

    def __init__(self, rules: list[Rule]) -> None:
        self.rules = rules

    def __call__(self, part: Part) -> str:
        for rule in self.rules:
            if (out := rule(part)) is not None:
                return out
        raise RuntimeError("Invalid rule")

    # pylint: disable=inconsistent-quotes
    def __repr__(self) -> str:
        return f"[{';'.join(str(rule) for rule in self.rules)}]"


def _parse_workflow(line: str) -> dict[str, Workflow]:
    name, raw = line.split("{")
    raw_rules = raw[:-1].split(",")
    rules = [Rule(rule) for rule in raw_rules]
    return {name: Workflow(rules)}


def _parse_part(line: str) -> Part:
    xmas = line.strip("}{").split(",")
    xmas = [int(attribute[2:]) for attribute in xmas]
    return Part(*xmas)


def load_data(path: str) -> tuple[dict[str, Workflow], list[Part]]:
    with open(path, "r") as f:
        workflows, parts = f.read().split("\n\n")
    workflows = reduce(or_, (_parse_workflow(line)
                             for line in workflows.splitlines()))
    parts = [_parse_part(line) for line in parts.splitlines()]
    return workflows, parts


def run_all_workflows(workflows: dict[str, Workflow], part: Part) -> str:
    key = "in"
    while key not in ("A", "R"):
        workflow = workflows[key]
        key = workflow(part)
    return key


def run(data: tuple[dict[str, Workflow], list[Part]]) -> int:
    workflows, parts = data
    accepted: list[Part] = []
    for part in parts:
        if run_all_workflows(workflows, part) == "A":
            accepted.append(part)
    return sum(part.total() for part in accepted)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 19114


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
