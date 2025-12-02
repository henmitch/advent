"""https://adventofcode.com/2025/day/2"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[tuple[int, int], ...]:
    with open(path, "r") as f:
        raw = f.read().split(",")
    return tuple(tuple(map(int, line.split("-"))) for line in raw)


def generate_valids(range_: tuple[int, int]) -> set[int]:
    start, end = range_
    out = set()
    l = len(str(start))
    if l == len(str(end)) and l%2:
        return out
    if l%2:
        base = "1" + "0"*(l//2)
    else:
        base = str(start)[:l//2]

    while True:
        testing = int(base*2)
        if testing > end:
            return out
        if testing >= start:
            out.add(testing)
        base = str(int(base) + 1)


def run(data: tuple[tuple[int, int], ...]) -> int:
    valids = set()
    for range_ in data:
        valids |= generate_valids(range_)
    return sum(valids)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 1227775554


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
