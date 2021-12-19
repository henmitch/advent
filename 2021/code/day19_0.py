"""https://adventofcode.com/2021/day/19"""
import itertools
from typing import List, Set, Tuple

import boilerplate as bp

Vector = Tuple[int, ...]
Matrix = Tuple[Vector]
Point = Tuple[int, int, int]
Pair = Tuple[int, int]
Scanner = List[Point]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> List[Scanner]:
    with open(path, "r") as f:
        raw = f.read().split("\n\n")
    out = []
    for raw_scanner in raw:
        raw_scanner = raw_scanner.splitlines()
        raw_scanner.pop(0)
        scanner = [
            tuple(int(x) for x in line.split(",")) for line in raw_scanner
        ]
        out.append(scanner)
    return out


# Distances between points will be invariant under rotation. So, we find the
# distances between all points as viewed by sensor A and as viewed by sensor B.
# Any points that are the same [distance from at least 12 other points] wrt A
# as wrt B will map to each other.
# We can then use those points to find the transform from A to B, apply that
# tranform to all the points in B, and then compare all that to C.


def get_distance(p1: Point, p2: Point) -> int:
    return sum(abs(a - b) for a, b in zip(p1, p2))
    # return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))


def get_distances(data: Scanner) -> Matrix:
    return tuple(set(get_distance(p1, p2) for p2 in data) for p1 in data)


def overlapping_idxes(l1: Scanner, l2: Scanner) -> List[List[Point]]:
    d1 = get_distances(l1)
    d2 = get_distances(l2)
    out = []
    for idx1, row1 in enumerate(d1):
        for idx2, row2 in enumerate(d2):
            if len(row1 & row2) >= 12:
                out.append((l1[idx1], l2[idx2]))
    return out


def duplicates(points: List[Tuple[Point, Point]]) -> List[Point]:
    left, right = zip(*points)
    left_dupes = [pair for pair in points if left.count(pair[0]) > 1]
    right_dupes = [pair for pair in points if right.count(pair[1]) > 1]
    return left_dupes + right_dupes


def deduplicated(data: List[Tuple[Point, Point]]) -> iter:
    for dupe in duplicates(data):
        yield list(set(data) - {dupe})


def find_mapping(points: List[List[Point]]) -> callable:
    """Find the function that maps each first point to each second point"""
    # If we have duplicates in either column, we need to deal with them.
    # For each set of duplicates:
    #   - Drop all other duplicates
    #   - Find mappings for each of the duplicates in the rest of the set
    #     - If there's only one mapping, use it
    #     - If there's more than one mapping, see which one works on the other
    #       duplicates.
    if duplicates(points):
        for dedeuped in deduplicated(points):
            maps = []
            try:
                maps.append(find_mapping(dedeuped))
            except ValueError:
                pass
        return max(maps, key=lambda m: maps.count(m))

    # First, we'll say we're done if each second point maps to its
    # corresponding first point.
    def successful(func: callable) -> bool:
        return all(func(p[1]) == p[0] for p in points)

    # It'll be some combination of translation, rotation, and reflection.

    # These are our options (not actual flips and rotations, just operations on
    # the indices)
    def flip_x(p: Point) -> Point:
        return (-p[0], p[1], p[2])

    def flip_y(p: Point) -> Point:
        return (p[0], -p[1], p[2])

    def flip_z(p: Point) -> Point:
        return (p[0], p[1], -p[2])

    def rotate_120(p: Point) -> Point:
        return (p[1], p[2], p[0])

    def rotate_201(p: Point) -> Point:
        return (p[2], p[0], p[1])

    def rotate_102(p: Point) -> Point:
        return (p[1], p[0], p[2])

    def rotate_210(p: Point) -> Point:
        return (p[2], p[1], p[0])

    def rotate_021(p: Point) -> Point:
        return (p[0], p[2], p[1])

    def identity(p: Point) -> Point:
        return p

    all_flips = [[flip, identity] for flip in [flip_x, flip_y, flip_z]]
    all_rotations = [
        rotate_120, rotate_201, rotate_102, rotate_210, rotate_021, identity
    ]
    # We're gonna go through all permutations of flips, plus each rotation
    # (and no rotation), then translate (such that the first second point maps
    # to the first first point). Then, we'll see if that's successful.
    for flips in itertools.product(*all_flips, all_rotations):
        # This covers everything twice, and can be improved
        flips = list(flips)
        rotation = flips.pop()

        def intermediate_func(p: Point) -> Point:
            for flip in flips:
                p = flip(p)
            p = rotation(p)
            return p

        lab, rat = points[0][0], intermediate_func(points[0][1])
        deltax, deltay, deltaz = (lab[0] - rat[0], lab[1] - rat[1],
                                  lab[2] - rat[2])

        def translate(p: Point) -> Point:
            return (p[0] + deltax, p[1] + deltay, p[2] + deltaz)

        def out_func(p: Point) -> Point:
            return translate(intermediate_func(p))

        if successful(out_func):
            return out_func
    raise ValueError("I'm out of ideas")


def merge(left: Scanner, right: Scanner) -> List[Point]:
    idxes = overlapping_idxes(left, right)
    if not idxes:
        return left
    mapping = find_mapping(idxes)
    return list(set(left) | set(mapping(p) for p in right))


def merge_all(data: List[Scanner]) -> Set[Point]:
    data = data.copy()
    out = data[0]
    while data:
        scanner = data.pop(0)
        before = len(out)
        out = merge(out, scanner)
        if len(out) == before and len(data) > 1:
            data.append(scanner)
    return set(out)


def test():
    data = load_data(TEST_PATH)
    assert len(merge_all(data)) == 79


def main():
    data = load_data(DATA_PATH)
    print(len(merge_all(data)))


if __name__ == "__main__":
    test()
    main()
