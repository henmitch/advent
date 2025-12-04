"""https://adventofcode.com/2025/day/3"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[tuple[int, ...]]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return tuple(tuple(int(x) for x in line) for line in raw)


def power_of_line(line: tuple[int, ...]) -> int:
    tens = max(line[:-1])
    ones = max(line[line.index(tens) + 1:])
    return tens*10 + ones


def run(data: tuple[int]) -> int:
    out = 0
    for line in data:
        out += power_of_line(line)
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 357


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
