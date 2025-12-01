"""https://adventofcode.com/2025/day/1"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[int]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return tuple(int(line.replace("L", " -")[1:]) for line in raw)


def run(data: tuple[int]) -> int:
    val = 50
    out = 0
    for num in data:
        val = (val + num)%100
        if not val:
            out += 1
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
