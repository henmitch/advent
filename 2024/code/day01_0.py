"""https://adventofcode.com/2024/day/1"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[list[int]]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    l, r = [], []
    for line in raw:
        s = line.split()
        l.append(int(s[0]))
        r.append(int(s[1]))
    return sorted(l), sorted(r)


def run(data: tuple[list[int]]) -> int:
    l, r = data
    out = 0
    for a, b in zip(l, r):
        out += abs(a - b)
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 11


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
