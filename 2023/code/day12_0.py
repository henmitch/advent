"""https://adventofcode.com/2023/day/12"""
from typing import Iterator

import boilerplate as bp

Line = tuple[str, list[int]]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[Line]:
    with open(path, "r") as f:
        lines = f.read().splitlines()
    out = [_parse(line) for line in lines]
    return out


def _parse(line: str) -> Line:
    springs, groups = line.split()
    groups = tuple(int(num) for num in groups.split(","))
    return springs, groups


# @functools.cache
def get_dot_counts(n_dots: int, n_groups: int) -> Iterator[list[int]]:
    if n_groups == 1:
        yield [n_dots]
        return
    for this_group in range(n_dots + 1):
        for rest in get_dot_counts(n_dots - this_group, n_groups - 1):
            yield [this_group] + rest


def generate_all(springs: str, groups: list[int]) -> list[str]:
    l = len(springs)
    blocks = [group*"#" for group in groups]
    n_dots = l - sum(groups)
    n_groups_of_dots = len(groups) + 1
    out = []
    for dot_counts in get_dot_counts(n_dots, n_groups_of_dots):
        if any(n == 0 for n in dot_counts[1:-1]):
            continue
        to_add = ""
        for dots, block in zip(dot_counts, blocks):
            to_add += dots*"." + block
        out.append(to_add + dot_counts[-1]*".")
    return out


def matches(springs: str, generated: str) -> bool:
    for s, g in zip(springs, generated):
        if s not in {"?", g}:
            return False
    return True


def count(springs: str, groups: list[int]) -> int:
    out = 0
    for generated in generate_all(springs, groups):
        if matches(springs, generated):
            out += 1
    return out


def run(data: list[Line]) -> int:
    return sum(count(*line) for line in data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 21


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    # test()
    main()
