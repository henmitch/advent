"""https://adventofcode.com/2022/day/10"""
import itertools
from collections import deque
from typing import Any

import boilerplate as bp
from day10_0 import DATA_PATH, DIRS, Pipes, load_data

TEST_PATH_08 = bp.get_test_path("08")
TEST_PATH_10 = bp.get_test_path("10")

ALL_DIRS = DIRS | {
    ns + ew: DIRS[ns] + DIRS[ew]
    for ns, ew in itertools.product(("N", "S"), ("E", "W"))
}
ADJACENTS = list(ALL_DIRS.values())
# There's a better way to do this, but this feels (relatively) readable
SEPARATES = {
    "|": (("NE", "E", "SE"), ("NW", "W", "SW")),
    "-": (("NE", "N", "NW"), ("SE", "S", "SW")),
    "L": (("NE", ), ("NW", "W", "SW", "S", "SE")),
    "J": (("NW", ), ("SW", "S", "SE", "E", "NE")),
    "7": (("SW", ), ("SE", "E", "NE", "N", "NW")),
    "F": (("SE", ), ("NE", "N", "NW", "W", "SW")),
}
SEPARATES = {
    key: tuple(tuple(ALL_DIRS[dir_] for dir_ in val) for val in group)
    for key, group in SEPARATES.items()
}
POINTS_AROUND = {
    key: set(dir_ for group in value for dir_ in group)
    for key, value in SEPARATES.items()
}


def get_other(s: Any, groups: tuple[tuple, tuple]) -> tuple:
    for group in groups:
        if s not in group:
            return group
    raise ValueError(f"{s} not found in {groups}")


def get_group(s: Any, groups: tuple[tuple, tuple]) -> tuple:
    for group in groups:
        if s in group:
            return group
    raise ValueError(f"{s} not found in {groups}")


def is_integral(c: complex) -> bool:
    return c.real == int(c.real) and c.imag == int(c.imag)


def get_both(s: Any, groups: tuple[tuple, tuple]) -> tuple[tuple, tuple]:
    if s in groups[0]:
        return groups
    if s in groups[1]:
        return groups[1], groups[0]
    raise ValueError(f"{s} not found in {groups}")


def make_all_ones(c: complex) -> complex:
    real, imag = c.real, c.imag
    if real:
        real = int(real/abs(real))
    if imag:
        imag = int(imag/abs(imag))
    return complex(real, imag)


def run(data: Pipes) -> int:
    pipes = Pipes(data)
    bounds = pipes.walk()

    # Walking along loop
    loc = bounds[1]
    pipe = pipes[loc]
    steps_for_left, steps_for_right = SEPARATES[pipe]
    left = {loc + l for l in steps_for_left if loc + l not in bounds}
    left |= {loc + l/2 for l in steps_for_left}
    right = {loc + r for r in steps_for_right if loc + r not in bounds}
    right |= {loc + r/2 for r in steps_for_right}
    just_found = left | right

    # At each boundary point...
    for loc in bounds[2:]:
        pipe = pipes[loc]
        # Look at all the points around it...
        points_to_check = {loc + pt for pt in POINTS_AROUND[pipe]}
        points_to_check |= {loc + pt/2 for pt in POINTS_AROUND[pipe]}
        points_to_check &= just_found
        next_point = points_to_check.pop()
        step = make_all_ones(next_point - loc)

        # Now, if the point we're looking at has already been identified as
        # left, we lump all other points in its sector (as determined by
        # the pipe) together as left, and everybody else is right.
        if next_point in left:
            steps_for_left, steps_for_right = get_both(step, SEPARATES[pipe])
        # Vice versa, otherwise
        elif next_point in right:
            steps_for_right, steps_for_left = get_both(step, SEPARATES[pipe])
        else:
            raise RuntimeError

        to_add_left = set()
        for l in steps_for_left:
            new_point = loc + l
            if new_point not in bounds:
                to_add_left.add(new_point)
            to_add_left.add(new_point - l/2)

        to_add_right = set()
        for r in steps_for_right:
            new_point = loc + r
            if new_point not in bounds:
                to_add_right.add(new_point)
            to_add_right.add(new_point - r/2)

        left |= to_add_left
        right |= to_add_right
        just_found = to_add_left | to_add_right

    frame = ([-1 + y*1j for y in range(pipes.height)] +
             [pipes.width + y*1j for y in range(pipes.height)] +
             [x - 1j for x in range(pipes.width)] +
             [x + pipes.height*1j for x in range(pipes.width)])
    to_check = deque(frame)

    # Moving in from the edge
    connected_to_edge = set()
    while to_check:
        current = to_check.popleft()
        connected_to_edge.add(current)
        for step in ADJACENTS:
            next_ = current + step
            for side in (left, right):
                if next_ in side:
                    inside = get_other(side, ((left, ), (right, )))[0]
                    to_check = deque([])
                    break
            else:
                if next_ in to_check:
                    continue
                if next_ in connected_to_edge:
                    continue
                if next_ in bounds:
                    continue
                if pipes.oob(next_):
                    continue

                to_check.append(next_)

    inside = {v for v in inside if is_integral(v)} - set(bounds)

    # Now, we go through everybody on the inside
    to_check = deque(inside)
    while to_check:
        current = to_check.popleft()
        for step in ADJACENTS:
            if (next_ := current + step) not in bounds and next_ not in inside:
                inside.add(next_)
                to_check.append(next_)

    return len(inside)


def pretty_print(pipes: Pipes, bounds: list[complex], inside: set[complex],
                 outside: set[complex]) -> str:
    out = ""
    for y, line in enumerate(pipes.data):
        for x, char in enumerate(line):
            loc = x + y*1j
            if loc in bounds:
                out += char
            elif loc in inside:
                out += "*"
            elif loc in outside:
                out += "."
            else:
                out += " "
        out += "\n"
    return out


def test():
    data = load_data(TEST_PATH_10)
    assert run(data) == 10
    data = load_data(TEST_PATH_08)
    assert run(data) == 8


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
