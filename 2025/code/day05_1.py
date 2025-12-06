"""https://adventofcode.com/2025/day/5"""
import boilerplate as bp
from day05_0 import TEST_PATH, DATA_PATH, Pair


def load_data(path: str) -> tuple[list[int], list[int]]:
    with open(path, "r") as f:
        ranges, _ = f.read().split("\n\n")
    mins, maxes = [], []
    for line in ranges.splitlines():
        low, high = (int(num) for num in line.split("-"))
        mins.append(low)
        maxes.append(high)
    return sorted(mins), sorted(maxes)


def combine_ranges(mins: list[int], maxes: list[int]) -> list[Pair]:
    combined = []
    while mins or maxes:
        current_min = mins.pop(0)
        while mins and (mins[0] <= maxes[0]):
            maxes.pop(0)
            mins.pop(0)
        current_max = maxes.pop(0)
        combined.append((current_min, current_max))
    return combined


def run(data: tuple[list[int], list[int]]) -> int:
    mins, maxes = data
    combined = combine_ranges(mins, maxes)
    out = 0
    for low, high in combined:
        out += high - low + 1
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 14


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
