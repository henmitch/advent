"""https://adventofcode.com/2023/day/17"""
from day17_0 import DATA_PATH, TEST_PATH, Array, load_data


def run(data: Array) -> int:
    return data.walk(range(4, 11))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 94


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
