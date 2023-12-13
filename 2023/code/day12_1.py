"""https://adventofcode.com/2023/day/12"""
from functools import cache

from day12_0 import DATA_PATH, TEST_PATH, Line, load_data


@cache
def get_placements(springs: str, groups: list[int]) -> int:
    # If we have no more groups to place...
    if len(groups) == 0:
        # There shouldn't be any '#' left
        if "#" in springs:
            return 0
        return 1

    # If we don't have enough springs left for groups + separation, it's
    # invalid
    if len(springs) < sum(groups) + len(groups) - 1:
        return 0

    # Ignore periods
    if springs[0] == ".":
        return get_placements(springs[1:], groups)

    out = 0
    current_idx = groups[0]
    # Try it both with a '.'...
    if springs[0] == "?":
        out += get_placements(springs[1:], groups)

    # And with a '#', if it makes sense
    if set(springs[:current_idx]) <= {"?", "#"}:
        if len(springs) <= current_idx or springs[current_idx] != "#":
            out += get_placements(springs[current_idx + 1:], groups[1:])

    return out


def run(data: list[Line]) -> int:
    return sum(
        get_placements("?".join(5*[spring]), 5*groups)
        for spring, groups in data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 525152


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
