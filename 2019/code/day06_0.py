"""https://adventofcode.com/2019/day/6"""
from operator import concat
from functools import reduce
import boilerplate as bp

Pair = tuple[str, str]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[Pair, ...]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return tuple(tuple(line.split(")")) for line in raw)


def checksum(orbits, depth: int = -1) -> int:
    if type(orbits) is str:
        return depth
    return sum(checksum(orbit, depth + 1) for orbit in orbits)


def build(pairs: tuple[Pair, ...], starter: tuple = ("COM", )):
    out = list(starter)
    filtered = set(filter(lambda x: x[0] in starter, pairs))
    if filtered:
        out += [
            list(reduce(concat,
                        (build(pairs, [pair[1]]) for pair in filtered)))
        ]
    return out


def run(data):
    built = build(data)
    return checksum(built)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 42


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
