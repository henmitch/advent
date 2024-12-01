"""https://adventofcode.com/2024/day/1"""
from day01_0 import DATA_PATH, TEST_PATH, load_data


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
