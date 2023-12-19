"""https://adventofcode.com/2023/day/18"""
from day18_0 import DATA_PATH, TEST_PATH, Instruction

DIRECTIONS = {"0": 1 + 0j, "1": 0 + 1j, "2": -1 + 0j, "3": 0 - 1j}


def load_data(path: str) -> list[Instruction]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return [_parse(line) for line in raw]


def _parse(line: str) -> Instruction:
    *_, instruction = line.split()
    instruction = instruction.strip("(#)")
    direction = instruction[-1]
    amount = int(instruction[:-1], 16)
    return DIRECTIONS[direction], amount


def find_coordinates(inst: list[Instruction]) -> list[complex]:
    loc = 0 + 0j
    centers = [loc]
    for direction, amount in inst:
        loc += amount*direction
        centers.append(loc)

    # To get the outer edges
    out = [-0.5j*inst[-1][0] - 0.5j*inst[0][0]]
    for (before, _), point, (after, _) in zip(inst, centers[1:], inst[1:]):
        out.append(point - 0.5j*before - 0.5j*after)

    return out


def _term(a: complex, b: complex) -> int:
    return (a.imag + b.imag)*(a.real - b.real)


def find_area_from_coordinates(coords: list[complex]) -> int:
    num = sum(_term(a, b) for a, b in zip(coords, coords[1:]))
    num += _term(coords[-1], coords[0])
    return int(abs(num/2))


def run(data: list[Instruction]) -> int:
    coordinates = find_coordinates(data)
    return find_area_from_coordinates(coordinates)


def test():
    data = load_data(TEST_PATH)
    out = run(data)
    assert out == 952408144115, out - 952408144115


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
