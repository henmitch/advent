"""https://adventofcode.com/2024/day/6"""
import operator

import boilerplate as bp

Axis = dict[int, list[int]]
Pair = tuple[complex, complex]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[Axis, Axis, complex, int, int]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    x_axis = {}
    y_axis = {}
    starter = 0 + 0j
    for y, line in enumerate(raw):
        for x, char in enumerate(line):
            if char == "#":
                x_axis[x] = x_axis.get(x, []) + [y]
                y_axis[y] = y_axis.get(y, []) + [x]
            if char == "^":
                starter = x + y*1j
    return x_axis, y_axis, starter, len(raw[0]), len(raw)


def walk(pos: complex, x_axis: Axis, y_axis: Axis, delta: complex, w: int,
         h: int) -> tuple[complex, bool]:
    x, y = int(pos.real), int(pos.imag)
    if delta.imag:
        axis = x_axis
        same, change = x, y
        mult = (1, 1j)
        maxer = h - 1
    elif delta.real:
        axis = y_axis
        same, change = y, x
        mult = (1j, 1)
        maxer = w - 1
    else:
        raise ValueError("Invalid direction")

    if delta.imag > 0 or delta.real > 0:
        # Down or right
        fun = min
        comp = operator.gt
    elif delta.imag < 0 or delta.real < 0:
        # Up or left
        fun = max
        comp = operator.lt
    else:
        raise ValueError("Invalid direction")

    can_hit = [loc for loc in axis.get(same, []) if comp(loc, change)]
    if not can_hit:
        return same*mult[0] + -fun([0, -maxer])*mult[1], True

    return same*mult[0] + fun(can_hit)*mult[1] - delta, False


def cross(a: Pair, b: Pair) -> bool:
    # Whether the line between two pairs of points crosses
    a1, a2 = a
    b1, b2 = b
    if a1.real == a2.real:
        # Vertical
        if b1.real == b2.real:
            # Both vertical
            return False
        # a is vertical, b is horizontal
        if min(a1.imag, a2.imag) <= b1.imag <= max(a1.imag, a2.imag):
            if min(b1.real, b2.real) <= a1.real <= max(b1.real, b2.real):
                return True
        return False
    # a is horizontal, b is vertical
    if min(a1.real, a2.real) <= b1.real <= max(a1.real, a2.real):
        if min(b1.imag, b2.imag) <= a1.imag <= max(b1.imag, b2.imag):
            return True
    return False


def run(data: tuple[Axis, Axis, complex, int, int]) -> int:
    x_axis, y_axis, pos, width, height = data
    direction = 0 - 1j
    seens: list[Pair] = []
    over = False
    while not over:
        end, over = walk(pos, x_axis, y_axis, direction, width, height)
        seens.append((pos, end))
        pos = end
        direction *= 1j

    crossings = 0
    for a in seens:
        for b in seens:
            if a == b:
                continue
            if cross(a, b):
                crossings += 1

    total_seens = sum(int(abs(a - b)) + 1 for a, b in seens)

    out = total_seens - crossings//2

    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 41


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
