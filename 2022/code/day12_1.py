"""https://adventofcode.com/2022/day/12"""
from itertools import product
from day12_0 import load_data, DATA_PATH, TEST_PATH, ElevationMap


def run(data: ElevationMap) -> int:
    out = data.width*data.height
    for x, y in product(range(data.width), range(data.height)):
        if data.value(x, y) == "a" and "b" in {
                data.value(*adj)
                for adj in data.allowed_steps(x, y)
        }:
            out = min(out, data.get_path_length((x, y)))
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 29


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    # test()
    main()
