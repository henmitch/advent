"""https://adventofcode.com/2020/day/21"""
import functools
import operator
import re

import boilerplate as bp

Pairing = tuple[set[str], set[str]]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path) -> tuple[Pairing]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    out = []
    for line in raw:
        match = re.match(r"(?P<gibberish>.*)\(contains (?P<allergens>.*)\)",
                         line)
        allergens = set(match["allergens"].split(", "))
        gibberish = set(match["gibberish"].split())
        out.append((allergens, gibberish))
    return out


def find_mapping(pairings: tuple[Pairing]) -> dict[str, set[str]]:
    out = {}
    for allergens, gibberish in pairings:
        for allergen in allergens:
            if allergen not in out:
                out[allergen] = set(gibberish)
            else:
                out[allergen] &= gibberish

    for allergen, ingredient in out.items():
        for comparator in out:
            if allergen == comparator:
                continue
            if len(ingredient) == 1:
                continue
            out[allergen] -= out[comparator]

    return out


def get_gibberish(pairings):
    gibberish = functools.reduce(operator.or_,
                                 (pairing[1] for pairing in pairings))
    return gibberish


def solos(mapping: dict[str, set[str]], pairings: tuple[Pairing]) -> set[str]:
    gibberish = get_gibberish(pairings)
    return gibberish - functools.reduce(operator.or_,
                                        (allergen
                                         for allergen in mapping.values()))


def count_solos(mapping: dict[str, set[str]], pairings: tuple[Pairing]) -> int:
    out = 0
    s = solos(mapping, pairings)
    for pairing in pairings:
        out += len(s & pairing[1])
    return out


def run(pairings: tuple[Pairing]) -> int:
    mapping = find_mapping(pairings)
    return count_solos(mapping, pairings)


def test():
    test_data = load_data(TEST_PATH)
    assert run(test_data) == 5


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
