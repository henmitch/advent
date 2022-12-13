"""https://adventofcode.com/2022/day/13"""
import json
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

Packet = list[int] | int


def compare(left: Packet, right: Packet) -> bool | None:
    # Both ints
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right

    # Both lists
    if isinstance(left, list) and isinstance(right, list):
        for l, r in zip(left, right):
            if (c := compare(l, r)) is not None:
                return c
        if len(left) == len(right):
            return None
        return len(left) < len(right)

    # Converting to lists if necessary
    left = left if isinstance(left, list) else [left]
    right = right if isinstance(right, list) else [right]
    return compare(left, right)


def load_data(path: str) -> list[tuple[Packet, Packet]]:
    with open(path, "r") as f:
        raw = f.read().strip().split("\n\n")
    return [tuple(map(json.loads, pair.split("\n"))) for pair in raw]


def run(data):
    out = 0
    for i, pair in enumerate(data):
        if compare(*pair):
            out += i + 1
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 13


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
