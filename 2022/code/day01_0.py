"""https://adventofcode.com/2022/day/1"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[tuple[int, ...], ...]:
    with open(path, "r") as f:
        raw = f.read().strip().split("\n\n")
    return tuple(tuple(map(int, chunk.split("\n"))) for chunk in raw)


def max_count(data: tuple[tuple[int, ...], ...]) -> int:
    return max(sum(chunk) for chunk in data)


def test():
    data = load_data(TEST_PATH)
    assert max_count(data) == 24000


def main():
    data = load_data(DATA_PATH)
    print(max_count(data))


if __name__ == "__main__":
    test()
    main()
