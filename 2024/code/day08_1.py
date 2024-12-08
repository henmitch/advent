"""https://adventofcode.com/2024/day/8"""
import itertools
from math import gcd

import boilerplate as bp
from day08_0 import DATA_PATH, TEST_PATH, is_oob, load_data


def antinodes(a: complex, b: complex, bound: tuple[int, int]) -> set[complex]:
    slope = b - a
    slope /= gcd(int(slope.real), int(slope.imag))
    out = set()
    # There's definitely a more efficient way to do this, but whatever
    adding = a
    while not is_oob(adding, bound):
        out.add(adding)
        adding += slope
    adding = b
    while not is_oob(adding, bound):
        out.add(adding)
        adding -= slope
    return out


def run(data: tuple[dict[str, list[complex]], tuple[int, int]]) -> int:
    locs = []
    nodes, bounds = data
    for _, positions in nodes.items():
        for a, b in itertools.combinations(positions, 2):
            locs.extend(antinodes(a, b, bounds))
    out = len(set(locs))
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 34


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
