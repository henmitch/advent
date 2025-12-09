"""https://adventofcode.com/2025/day/9"""
import itertools
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

Pair = tuple[int, int]


def load_data(path: str) -> list[Pair]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return [tuple(int(v) for v in line.split(",")) for line in raw]


def area(a: Pair, b: Pair) -> int:
    return abs((a[0] - b[0] + 1)*(a[1] - b[1] + 1))


def run(data: tuple[int]) -> int:
    return max(area(a, b) for a, b in itertools.combinations(data, 2))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 50


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
