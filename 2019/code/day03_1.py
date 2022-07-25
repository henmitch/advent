"""https://adventofcode.com/2019/day/3"""
import boilerplate as bp

Line = set[complex]
Mapping = dict[complex, int]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[Line, ...]:
    with open(path, "r") as f:
        raw = f.readlines()
    return tuple(interpret(line) for line in raw)


def interpret(line: str) -> tuple[Line, Mapping]:
    current = 0 + 0j
    taken_so_far = 0
    taken = {}
    out = set()
    directions = {"U": 0 + 1j, "R": 1 + 0j, "D": 0 - 1j, "L": -1 + 0j}
    for command in line.split(","):
        direction = directions[command[0]]
        n_steps = int(command[1:])
        for step in range(1, n_steps + 1):
            taken_so_far += 1
            taken[current + step*direction] = taken_so_far

        out |= set(taken.keys())
        current = current + n_steps*direction
    return out, taken


def find_overlaps(data: tuple[tuple[Line, Mapping], ...]) -> Mapping:
    out = {}
    (line1, mapping1), (line2, mapping2) = data
    for point in line1 & line2:
        out[point] = mapping1[point] + mapping2[point]
    return out


def minimum_steps(overlaps: Mapping) -> int:
    return min(overlaps.values())


def run(data: tuple[Line, ...]) -> int:
    overlaps = find_overlaps(data)
    return minimum_steps(overlaps)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 610


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
