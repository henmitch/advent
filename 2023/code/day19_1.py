"""https://adventofcode.com/2023/day/19"""
from __future__ import annotations

import itertools
from dataclasses import asdict, astuple, dataclass
from functools import cache

from day19_0 import DATA_PATH, TEST_PATH, Rule, Workflow

Workflows = list[tuple[str, Workflow]]


@dataclass
class GenericPart:
    x: tuple[int, int]
    m: tuple[int, int]
    a: tuple[int, int]
    s: tuple[int, int]

    def __init__(self) -> None:
        self.x = self.m = self.a = self.s = (1, 4000)

    def empty(self) -> None:
        self.x = self.m = self.a = self.s = (0, 0)

    def apply(self, rule: Rule) -> None:
        min_, max_ = getattr(self, rule.category)
        if rule.comparison == ">":
            setattr(self, rule.category, (max(min_, rule.target + 1), max_))
        elif rule.comparison == "<":
            setattr(self, rule.category, (min_, min(rule.target - 1, max_)))
        else:
            raise RuntimeError(f"Invalid rule {rule} applied to {self}")

    def n_parts(self) -> int:
        out = 1
        for min_, max_ in astuple(self):
            if min_ == max_:
                return 0
            out *= max_ - min_ + 1
        return out

    def overlaps_with(self, part: GenericPart) -> bool:
        return all(overlap(s, p) for s, p in zip(astuple(self), astuple(part)))

    def get_overlap(self, part: GenericPart) -> GenericPart:
        out = GenericPart()
        if not self.overlaps_with(part):
            out.empty()
            return out
        part = asdict(part)
        for category, mine in asdict(self).items():
            theirs = part[category]
            low = max(mine[0], theirs[0])
            high = min(mine[1], theirs[1])
            setattr(out, category, (low, high))
        return out

    def contains(self, part: GenericPart) -> bool:
        return all(s[0] <= p[0] and s[1] >= p[1]
                   for s, p in zip(astuple(self), astuple(part)))

    def is_contained_by(self, part: GenericPart) -> bool:
        return part.contains(self)


def load_data(path: str) -> Workflows:
    with open(path, "r") as f:
        workflows, _ = f.read().split("\n\n")
    workflows = tuple(_parse_workflow(line) for line in workflows.splitlines())
    return workflows


def _parse_workflow(line: str) -> tuple[str, Workflow]:
    name, raw = line.split("{")
    raw_rules = raw[:-1].split(",")
    rules = [Rule(rule) for rule in raw_rules]
    return (name, Workflow(rules))


def paths_to(point: str, workflows: Workflows) -> list[list[str, Rule]]:
    out = []
    for name, workflow in workflows:
        inverses = []
        for rule in workflow.rules[:-1]:
            if rule.output == point:
                out.append([name] + inverses + [rule])
            else:
                inverses.append(rule.inverse())
        default = workflow.rules[-1]
        if default.output == point:
            out.append([name] + inverses)
    return out


@cache
def all_paths_to(point: str, workflows: Workflows) -> list[list[str | Rule]]:
    if point == "in":
        return [[]]
    out = []
    paths = paths_to(point, workflows)
    for name, *path_so_far in paths:
        to_adds = all_paths_to(name, workflows)
        for to_add in to_adds:
            out.append(to_add + path_so_far)
    return out


def overlap(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] <= b[0] <= a[1] or a[0] <= b[1] <= a[1]


def run(data: Workflows, end: str = "A") -> int:
    paths_to_end = all_paths_to(end, data)
    parts: list[GenericPart] = []
    for path in paths_to_end:
        part = GenericPart()
        for rule in path:
            part.apply(rule)
        parts.append(part)
    n_parts = sum(part.n_parts() for part in parts)

    overlaps: list[GenericPart] = []
    for a, b in itertools.combinations(parts, 2):
        if a == b:
            print(f"{a} is {b}")
        # elif a.contains(b):
        #     print(f"{a} contains {b}")
        # elif b.contains(a):
        #     print(f"{b} contains {a}")
        overlaps.append(a.get_overlap(b))
    n_overlaps = sum(overlap.n_parts() for overlap in overlaps)
    return n_parts - n_overlaps


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
