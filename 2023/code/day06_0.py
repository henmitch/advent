"""https://adventofcode.com/2023/day/6"""
import math
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[list[int], list[int]]:
    with open(path, "r") as f:
        times, distances = f.read().splitlines()
    return _parse(times), _parse(distances)


def _parse(line: str) -> list[int]:
    return list(map(int, line.split()[1:]))


def race(time: int, distance: int) -> int:
    # Doing ceil/-1 and floor/+1 because we need to *beat* the record, not
    # just tie it
    max_win = math.ceil((time + math.sqrt(time**2 - 4*distance))/2) - 1
    min_win = math.floor((time - math.sqrt(time**2 - 4*distance))/2) + 1
    return max_win - min_win + 1  # +1 to include endpoints


def run(data: tuple[list[int], list[int]]) -> int:
    out = 1
    for time, distance in zip(*data):
        out *= race(time, distance)
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 288


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
