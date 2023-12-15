"""https://adventofcode.com/2023/day/15"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[str]:
    with open(path, "r") as f:
        out = f.read()
    out = out.strip().split(",")
    return out


def hashify(line: str) -> int:
    out = 0
    for s in line:
        out += ord(s)
        out *= 17
        out = out%256
    return out


def run(data: list[str]) -> int:
    return sum(hashify(s) for s in data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 1320


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
