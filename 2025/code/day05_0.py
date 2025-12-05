"""https://adventofcode.com/2025/day/5"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

Pair = tuple[int, int]
Pairs = tuple[Pair, ...]


def load_data(path: str) -> tuple[Pairs, tuple[int, ...]]:
    with open(path, "r") as f:
        ranges, values = f.read().split("\n\n")
    ranges = tuple(
        tuple(int(num)
              for num in line.split("-"))
        for line in ranges.splitlines())
    values = tuple(int(line) for line in values.splitlines())
    return ranges, values


def run(data: tuple[Pairs, tuple[int, ...]]) -> int:
    ranges, values = data
    out = 0
    for val in values:
        for low, high in ranges:
            if low <= val <= high:
                out += 1
                break
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 3


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
