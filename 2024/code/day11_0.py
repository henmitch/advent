"""https://adventofcode.com/2024/day/11"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[int]:
    with open(path, "r") as f:
        raw = f.read().strip()
    return [int(x) for x in raw.split()]


def split(val: int) -> tuple[int, int]:
    l = len(str(val))
    return int(str(val)[:l//2]), int(str(val)[l//2:])


def process(val: int) -> list[int]:
    if val == 0:
        return [1]
    if not len(str(val))%2:
        return list(split(val))
    return [2024*val]


def run(data: list[int]) -> int:
    # Naive approach
    for _ in range(25):
        data = [x for val in data for x in process(val)]
    return len(data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 55312


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
