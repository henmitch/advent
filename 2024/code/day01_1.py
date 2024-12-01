"""https://adventofcode.com/2024/day/1"""
import boilerplate as bp
from day01_0 import load_data

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def run(data: tuple[list[int], list[int]]) -> int:
    l, r = data
    out = 0
    for a in l:
        out += a*r.count(a)
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 31


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
