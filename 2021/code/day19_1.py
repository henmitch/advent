"""https://adventofcode.com/2021/day/19"""
from typing import List, Tuple

import day19_0 as old


def scanner_location(s1: old.Scanner, s2: old.Scanner) -> old.Point:
    idxes = list(set(old.overlapping_idxes(s1, s2)))
    if not idxes:
        raise ValueError("No overlapping points")
    mapping = old.find_mapping(idxes)
    return mapping((0, 0, 0))


def largest_distance(locations: List[old.Point]) -> int:
    distances = old.get_distances(locations)
    return max(max(row) for row in distances)


def find_locations(scanners: List[old.Scanner]) -> Tuple[old.Point]:
    merged = tuple(old.merge_all(scanners))
    locations = tuple(scanner_location(merged, s) for s in scanners)
    return locations


def answer(scanners: List[old.Scanner]) -> int:
    locations = find_locations(scanners)
    return largest_distance(locations)


def test():
    data = old.load_data(old.TEST_PATH)
    assert answer(data) == 3621


if __name__ == "__main__":
    test()
    data = old.load_data(old.DATA_PATH)[::-1]
    print(answer(data))
