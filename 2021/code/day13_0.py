"""https://adventofcode.com/2021/day/13"""
from typing import List, Set, Tuple

import boilerplate as bp

DATA_PATH = bp.get_data_path()
TEST_PATH = bp.get_test_path()


def load_data(path):
    with open(path, "r") as f:
        input_ = f.read()

    points_raw, folds_raw = input_.split("\n\n")

    points_raw = points_raw.split("\n")
    points = set(tuple(map(int, point.split(","))) for point in points_raw)

    folds = []
    for fold_raw in folds_raw.split("\n"):
        direction, location = fold_raw.split("=")
        folds.append((direction[-1], int(location)))

    return points, folds


def fold_up(point: Tuple[int], fold_: int) -> Set[tuple]:
    if fold_ > point[1]:
        return {
            point,
        }

    return {
        (point[0], fold_ - (point[1] - fold_)),
    }


def fold_left(point: Tuple[int], fold_: Tuple[int]) -> Set[tuple]:
    if fold_ > point[0]:
        return {
            point,
        }

    return {
        (fold_ - (point[0] - fold_), point[1]),
    }


def fold(points: Set[Tuple[int]], folds: List[Tuple[int]]) -> Set[Tuple[int]]:
    out = set()
    direction, location = folds[0]
    for point_x, point_y in points:
        if direction == "x":
            out |= fold_left((point_x, point_y), location)
        else:
            out |= fold_up((point_x, point_y), location)
    if len(folds) > 1:
        return fold(out, folds[1:])
    return out


def count_dots_after_fold(points, folds):
    return len(fold(points, folds))


def pretty_print(points: Set[Tuple[int]]):
    x_max = max(x for x, _ in points)
    y_max = max(y for _, y in points)
    out = [["." for _ in range(x_max + 1)] for __ in range(y_max + 1)]
    for point in points:
        out[point[1]][point[0]] = "#"
    return "\n".join(" ".join(row) for row in out) + "\n"


def test():
    points, folds = load_data(TEST_PATH)
    assert count_dots_after_fold(points, [folds[0]]) == 17


def main():
    points, folds = load_data(DATA_PATH)
    print(count_dots_after_fold(points, [folds[0]]))


if __name__ == "__main__":
    test()
    main()
