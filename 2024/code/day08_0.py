"""https://adventofcode.com/2024/day/8"""
import itertools

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[dict[str, list[complex]], tuple[int, int]]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    out = {}
    for y, line in enumerate(raw):
        for x, char in enumerate(line):
            if char == ".":
                continue
            out[char] = out.get(char, []) + [x + y*1j]
    return out, (len(raw[0]), len(raw))


def antinodes(a: complex, b: complex) -> tuple[complex, complex]:
    diff = b - a
    return a - diff, b + diff


def is_oob(pos: complex, bounds: tuple[int, int]) -> bool:
    return not (0 <= pos.real < bounds[0] and 0 <= pos.imag < bounds[1])


def run(data: tuple[dict[str, list[complex]], tuple[int, int]]) -> int:
    locs = []
    nodes, bounds = data
    for _, positions in nodes.items():
        for a, b in itertools.combinations(positions, 2):
            locs.extend(anti for anti in antinodes(a, b)
                        if not is_oob(anti, bounds))
    out = len(set(locs))
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
