"""https://adventofcode.com/2022/day/18"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

Cube = tuple[int, int, int]


def load_data(path: str) -> set[Cube]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    out = set()
    for line in raw:
        out.add(tuple(map(int, line.split(","))))
    return out


def neighbors(cube: Cube) -> set[Cube]:
    out = set()
    for i in range(3):
        for add in [-1, 1]:
            out.add(cube[:i] + (cube[i] + add, ) + cube[i + 1:])
    return out


def run(data: set[Cube]) -> int:
    out = 0
    for cube in data:
        out += len(neighbors(cube) - data)
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 64


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
