"""https://adventofcode.com/2022/day/4"""
import boilerplate as bp

Bounds = tuple[int, int]
Pair = tuple[Bounds, Bounds]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[Pair]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return list(map(list_bounds, raw))


def list_bounds(pair: str) -> Pair:
    # Not using set math just in case inputs are huge
    return tuple(map(lambda x: tuple(map(int, x.split("-"))), pair.split(",")))


def completely_overlaps(pair: Pair) -> bool:
    [l1, h1], [l2, h2] = pair
    return (l1 <= l2 and h1 >= h2) or (l1 >= l2 and h1 <= h2)


def run(data: list[Pair]):
    return sum(map(completely_overlaps, data))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 2


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
