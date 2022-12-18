"""https://adventofcode.com/2022/day/18"""
from itertools import product
from day18_0 import DATA_PATH, TEST_PATH, Cube, load_data, neighbors


def expanded(cube: Cube) -> set[Cube]:
    x, y, z = cube
    out = {(x + add_x, y + add_y, z + add_z)
           for add_x, add_y, add_z in product(*[[-1, 0, 1]]*3)}
    return out - {cube}


def get_surface(data: set[Cube]) -> set[Cube]:
    out = []
    for cube in data:
        out += list(expanded(cube) - data)
    return set(out)


def leftest_point(data: set[Cube]) -> Cube:
    # Guaranteed to be on the outside
    return min(data)


def accessible_points(start: Cube, other_points: set[Cube]) -> set[Cube]:
    to_check = neighbors(start) & other_points
    out = {start}
    while to_check:
        surface_cube = to_check.pop()
        if surface_cube in out:
            continue
        out.add(surface_cube)
        to_check |= (neighbors(surface_cube) & other_points)
    return out


def run(data: set[Cube]) -> int:
    surface = get_surface(data)
    start = leftest_point(surface)
    outside = accessible_points(start, surface)
    out = 0
    for cube in data:
        for neighbor in neighbors(cube):
            if neighbor in outside:
                out += 1
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 58


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
