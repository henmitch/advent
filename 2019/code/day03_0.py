"""https://adventofcode.com/2019/day/3"""
import boilerplate as bp

Line = set[complex]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[Line, ...]:
    with open(path, "r") as f:
        raw = f.readlines()
    return tuple(interpret(line) for line in raw)


def interpret(line: str) -> Line:
    current = 0 + 0j
    out = set()
    directions = {"U": 0 + 1j, "R": 1 + 0j, "D": 0 - 1j, "L": -1 + 0j}
    for command in line.split(","):
        direction = directions[command[0]]
        n_steps = int(command[1:])
        to_add = {current + step*direction for step in range(1, n_steps + 1)}
        out |= to_add
        current = current + n_steps*direction
    return out


def find_overlaps(lines: tuple[Line]) -> set[complex]:
    out = set()
    for i, line in enumerate(lines[:-1]):
        for comparison in lines[i + 1:]:
            out |= line & comparison
    return out


def minimum_distance(overlaps: set[complex]) -> int:
    return int(min(abs(over.real) + abs(over.imag) for over in overlaps))


def run(data: tuple[Line, ...]) -> int:
    overlaps = find_overlaps(data)
    return minimum_distance(overlaps)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 159


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
