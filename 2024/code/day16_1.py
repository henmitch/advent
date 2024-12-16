"""https://adventofcode.com/2024/day/16"""
import boilerplate as bp
from day16_0 import DATA_PATH, TEST_PATH_0, load_data


def run(data: ...) -> int:
    return ...


def test():
    data = load_data(TEST_PATH_0)
    assert run(data) == ...


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
