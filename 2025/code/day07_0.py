"""https://adventofcode.com/2025/day/7"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[str]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return raw


def run(data: str) -> int:
    out = 0
    current = {data[0].index("S")}
    for row in data[1:]:
        next_ = set()
        for j, val in enumerate(row):
            if j in current:
                if val == "^":
                    next_ |= {j - 1, j + 1}
                    out += 1
                else:
                    next_ |= {j}
        current = next_
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 21


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
