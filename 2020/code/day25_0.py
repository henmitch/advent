"""https://adventofcode.com/2020/day/25"""
import itertools
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[int, int]:
    with open(path, "r") as f:
        return tuple(int(i) for i in f.readlines())


def take_next(current: int, subject_number: int = 7) -> int:
    return (current*subject_number)%20201227


def get_loop_size(public_key: int) -> int:
    current = 1
    loop_size = 0
    while current != public_key:
        current = take_next(current)
        loop_size += 1
    return loop_size


def run(vals: tuple[int, int]) -> int:
    door_public_key, card_public_key = vals
    door_loop_size = get_loop_size(door_public_key)
    out = 1
    for _ in range(door_loop_size):
        out = take_next(out, card_public_key)
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 14897079


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
