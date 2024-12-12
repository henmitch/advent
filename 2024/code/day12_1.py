"""https://adventofcode.com/2024/day/12"""
import boilerplate as bp
from day12_0 import (DATA_PATH, TEST_PATH_0, TEST_PATH_2, Garden, load_data,
                     score)

TEST_PATH_3 = bp.get_test_path("3")
TEST_PATH_4 = bp.get_test_path("4")

DIAGONALS = [1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]


def number_of_sides(region: set[complex]) -> int:
    # Equivalent to the number of corners
    out = 0
    for pos in region:
        n_corners = 0
        neighbors = {pos + c for c in Garden.CARDINALS}
        for d in DIAGONALS:
            diag = pos + d
            shared = {diag + c for c in Garden.CARDINALS} & neighbors
            # if diag not in region and not any(n in region for n in shared):
            if all(n not in region for n in shared):
                n_corners += 1
            elif diag not in region and all(n in region for n in shared):
                n_corners += 1
        out += n_corners

    return out


def run(data: Garden) -> int:
    # First, separate the data into continguous regions
    regions = {}
    for pos, cell in data:
        regions[pos] = regions.get(pos, set()) | {pos}
        for n in data.neighbors(pos):
            if data.oob(n):
                continue
            if data[n] == cell:
                regions[pos] = regions[pos] | {n} | regions.get(n, set())
                for loc in regions[pos]:
                    regions[loc] = regions[pos]

    for region, locs in regions.items():
        regions[region] = frozenset(locs)

    # Then, calculate the area and perimeter of each region
    areas = {v: len(v) for v in regions.values()}
    sideses = {v: number_of_sides(v) for v in regions.values()}
    out = score(areas, sideses)
    return out


def test():
    data_0 = load_data(TEST_PATH_0)
    assert run(data_0) == 80
    data_3 = load_data(TEST_PATH_3)
    assert run(data_3) == 236
    data_4 = load_data(TEST_PATH_4)
    assert run(data_4) == 368
    data_2 = load_data(TEST_PATH_2)
    assert run(data_2) == 1206


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
