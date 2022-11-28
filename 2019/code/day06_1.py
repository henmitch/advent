"""https://adventofcode.com/2019/day/6"""
from operator import concat
from functools import reduce
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> dict:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return dict(reversed(line.split(")")) for line in raw)


def depth(orbits: dict, to_find: str) -> set[str]:
    found = orbits[to_find]
    out = {found}
    while found != "COM":
        found = orbits[found]
        out |= {found}
    return out


def path_length(orbits: dict, start: str = "YOU", end: str = "SAN") -> int:
    s = depth(orbits, start)
    e = depth(orbits, end)
    return len((s | e) - (s & e))


def test():
    data = load_data(TEST_PATH)
    data |= {"YOU": "K", "SAN": "I"}
    assert path_length(data) == 4


def main():
    data = load_data(DATA_PATH)
    print(path_length(data))


if __name__ == "__main__":
    test()
    main()
