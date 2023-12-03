"""https://adventofcode.com/2023/day/3"""
import itertools
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

NUMBERS = set(map(str, range(10)))
IGNORES = NUMBERS | {"."}


def load_data(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def get_buddies(data: list[str], row_num: int, col_num: int) -> set[str]:
    out = set()
    for i, j in itertools.product([0, 1], [0, 1]):
        if i == j == 0:
            continue
        x_min = max(col_num - j, 0)
        x_max = min(col_num + j, len(data[0]) - 1)
        y_min = max(row_num - i, 0)
        y_max = min(row_num + i, len(data[0]) - 1)
        out |= {
            data[y][x]
            for x, y in itertools.product((x_min, x_max), (y_min, y_max))
        }
    return out


def run(data: list[str]) -> int:
    total = 0
    width = len(data[0])
    for row_num, row in enumerate(data):
        col_num = 0
        while col_num < width:
            char = row[col_num]
            if char not in NUMBERS:
                col_num += 1
                continue
            current_num = ""
            buddies = set()
            while col_num < width and row[col_num] in NUMBERS:
                current_num += row[col_num]
                # Check around the current digit
                buddies |= get_buddies(data, row_num, col_num)
                col_num += 1
            if buddies - IGNORES:
                total += int(current_num)
    return total


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 4361


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
