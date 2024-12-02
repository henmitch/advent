"""https://adventofcode.com/2024/day/2"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[list[int]]:
    with open(path, "r") as f:
        raw = f.readlines()
    return [list(map(int, x.split())) for x in raw]


def is_safe(line: list[int]) -> bool:
    try:
        direction = (line[1] - line[0])/abs(line[1] - line[0])
    except ZeroDivisionError:
        return False
    for a, b in zip(line, line[1:]):
        if b - a not in (direction, 2*direction, 3*direction):
            return False
    return True


def run(data: list[list[int]]) -> int:
    return sum(is_safe(x) for x in data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 2


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
