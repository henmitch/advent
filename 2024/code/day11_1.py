"""https://adventofcode.com/2024/day/11"""
from collections import Counter

import boilerplate as bp
from day11_0 import DATA_PATH, process


def load_data(path: str) -> dict[int, int]:
    with open(path, "r") as f:
        raw = f.read().strip()
    return Counter([int(x) for x in raw.split()])


def step(data: dict[int, int]) -> dict[int, int]:
    out = {}
    for val, count in data.items():
        for new_val in process(val):
            out[new_val] = out.get(new_val, 0) + count
    return out


def run(data: dict[int, int]) -> int:
    for _ in range(75):
        data = step(data)
    return sum(data.values())


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    # No value for the test gase given
    main()
