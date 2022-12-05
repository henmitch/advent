"""https://adventofcode.com/2022/day/4"""
import boilerplate as bp
from day04_0 import load_data, TEST_PATH, DATA_PATH, Pair, completely_overlaps


def partly_overlaps(pair: Pair) -> bool:
    [l1, h1], [l2, h2] = pair
    return ((l1 <= l2 and h1 >= l2) or (l1 >= l2 and l1 <= h2)
            or completely_overlaps(pair))


def run(data: list[Pair]):
    return sum(map(partly_overlaps, data))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 4


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
