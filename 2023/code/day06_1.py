"""https://adventofcode.com/2023/day/6"""
from day06_0 import race, TEST_PATH, DATA_PATH


def load_data(path: str) -> tuple[int, int]:
    with open(path, "r") as f:
        times, distances = f.read().splitlines()
    return _parse(times), _parse(distances)


def _parse(line: str) -> int:
    return int("".join(line.split()[1:]))


def run(data: tuple[int, int]) -> int:
    return race(*data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 71503


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
