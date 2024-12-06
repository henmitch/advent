"""https://adventofcode.com/2024/day/6"""
import boilerplate as bp
from day06_0 import DATA_PATH, TEST_PATH, Axis, Pair, load_data, walk


def sign(x: int) -> int:
    return (x > 0) - (x < 0)


def points_between(a: complex, b: complex) -> list[complex]:
    if a.imag == b.imag:
        s = sign(b.real - a.real)
        return [a + s*x for x in range(1, int(abs(a.real - b.real)) + 1)]
    if a.real == b.real:
        s = sign(b.imag - a.imag)
        return [a + s*x*1j for x in range(1, int(abs(a.imag - b.imag)) + 1)]
    raise ValueError("Points must be on the same axis")


def add_to_axes(x_axis: Axis, y_axis: Axis,
                point: complex) -> tuple[Axis, Axis]:
    x, y = int(point.real), int(point.imag)
    new_x_axis = x_axis.copy()
    new_y_axis = y_axis.copy()
    new_x_axis[x] = x_axis.get(x, []) + [y]
    new_y_axis[y] = y_axis.get(y, []) + [x]
    return new_x_axis, new_y_axis


def forms_loop(x_axis: Axis, y_axis: Axis, pos: complex, width: int,
               height: int) -> bool:
    direction = 0 - 1j
    ends: list[Pair] = [[pos, direction]]
    over = False
    while not over:
        end, over = walk(pos, x_axis, y_axis, direction, width, height)
        direction *= 1j
        pos = end
        if [pos, direction] in ends:
            return True
        ends.append([end, direction])

    return False


def run(data: tuple[Axis, Axis, complex, int, int]) -> int:
    x_axis, y_axis, start, width, height = data
    pos = start
    direction = 0 - 1j
    endses: list[Pair] = []
    over = False
    while not over:
        end, over = walk(pos, x_axis, y_axis, direction, width, height)
        endses.append((pos, end))
        pos = end
        direction *= 1j

    blockers: set[complex] = set()
    for a, b in endses:
        for point in points_between(a, b):
            new_x_axis, new_y_axis = add_to_axes(x_axis, y_axis, point)
            if forms_loop(new_x_axis, new_y_axis, start, width, height):
                blockers.add(point)
    out = len(blockers)
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 6


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
