"""https://adventofcode.com/2024/day/03"""
import boilerplate as bp
from day03_0 import DATA_PATH, Pair, parse, run

TEST_PATH = bp.get_test_path("1")


def load_data(path: str) -> list[list[Pair]]:
    with open(path, "r") as f:
        raw = f.read()
    raw = ("do()" + raw).replace("\n", "")\
        .replace("do()", "\ndo()")\
        .replace("don't()", "\ndon't()").splitlines()
    return find_dos(raw)


def find_dos(data: list[str]) -> list[Pair]:
    dos = list(filter(lambda x: x.startswith("do()"), data))
    return parse("".join(dos))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 48


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
