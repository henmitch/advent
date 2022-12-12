"""https://adventofcode.com/2022/day/9"""
from day09_0 import load_data, DATA_PATH, TEST_PATH, DIRECTIONS


def step(direction: complex, knots: list[complex]) -> list[complex]:
    # First knot will always move in the given direction
    out = [knots[0] + direction]
    while len(out) < len(knots):
        # Most recently moved knot
        k1 = out[-1]
        # The knot after the most recently moved knot
        k2 = knots[len(out)]
        diff = k1 - k2
        # First, check and see if they're too far apart. If not, we don't need
        # to do anything
        if abs((diff).real) <= 1 and abs((diff).imag) <= 1:
            out.append(k2)
            continue
        # Next, let's handle the horizontal/vertical cases
        if diff == 2*direction:
            k2 += direction
            out.append(k2)
            continue
        # Finally, the diagonal cases. We move k2 in the direction of greatest
        # difference
        k2 += sign(diff)
        out.append(k2)
    return out


def sign(x: complex) -> complex:
    out = 0
    if x.real:
        out += x.real/abs(x.real)
    if x.imag:
        out += x.imag*1j/abs(x.imag)
    return out


def move(instruction: tuple[str, int],
         knots: list[complex]) -> tuple[list[complex], set[complex]]:
    direction = DIRECTIONS[instruction[0]]
    distance = instruction[1]
    out = {knots[-1]}
    for _ in range(distance):
        knots = step(direction, knots)
        out.add(knots[-1])
    return knots, out


def run(data: list[tuple[str, int]]) -> int:
    knots = 10*[0]
    out = {0}
    for row in data:
        knots, to_add = move(row, knots)
        out |= to_add
    return len(out)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 1
    new_data = [("R", 5), ("U", 8), ("L", 8), ("D", 3), ("R", 17), ("D", 10),
                ("L", 25), ("U", 20)]
    assert run(new_data) == 36


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
