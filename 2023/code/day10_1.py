"""https://adventofcode.com/2022/day/10"""
import itertools
from collections import deque

import boilerplate as bp
from day10_0 import DATA_PATH, DIRS, PIPES, Pipes, load_data

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


def get_other(s: str, groups: tuple[tuple, tuple]) -> tuple:
    for group in groups:
        if s not in group:
            return group
    raise ValueError(f"{s} not found in {groups}")


def get_group(s: str, groups: tuple[tuple, tuple]) -> tuple:
    for group in groups:
        if s in group:
            return group
    raise ValueError(f"{s} not found in {groups}")


def is_integral(c: complex) -> bool:
    return all(v == int(v) for v in [c.real, c.imag])


def run(data: Pipes) -> int:
    pipes = Pipes(data)
    bounds = pipes.walk()
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
            if pipes.oob(next_):
                continue
            if next_ in bounds:
                continue
            if next_ in connected_to_edge:
                continue
            if next_ in to_check:
                continue

            to_check.append(next_)

    # print(pretty_print(pipes, bounds, set(), connected_to_edge))

    # Walking along loop
    known_inside = set()
    known_outside = connected_to_edge
    to_check = deque(bounds)
    while to_check:
        loc = to_check.popleft()
        pipe = pipes[loc]
        if pipe == "S":
            continue
        # Check if any non-pipe neighbors are known
        for dir_, step in ALL_DIRS.items():
            if dir_ in PIPES[pipe]:
                continue
            if loc + step in bounds:
                step /= 2
            if loc + step in known_outside:
                add_to_in = get_other(dir_, SEPARATES[pipe])
                add_to_out = get_group(dir_, SEPARATES[pipe])
                break
            if loc + step in known_inside:
                add_to_in = get_group(dir_, SEPARATES[pipe])
                add_to_out = get_other(dir_, SEPARATES[pipe])
                break
        else:
            if loc not in to_check and loc not in bounds:
                to_check.append(loc)
            continue
        for in_ in add_to_in:
            if pipes.oob(loc + ALL_DIRS[in_]):
                continue
            known_inside.add(loc + ALL_DIRS[in_])
            known_inside.add(loc + ALL_DIRS[in_]/2)
        for out in add_to_out:
            # if pipes.oob(loc + ALL_DIRS[out]):
            #     continue
            known_outside.add(loc + ALL_DIRS[out])
            known_outside.add(loc + ALL_DIRS[out]/2)

    known_inside = {v for v in known_inside if is_integral(v)} - set(bounds)
    print(pretty_print(pipes, bounds, known_inside, known_outside))
    return len(known_inside)


def pretty_print(pipes: Pipes, bounds: list[complex],
                 known_inside: set[complex],
                 known_outside: set[complex]) -> str:
    out = ""
    for y, line in enumerate(pipes.data):
        for x, char in enumerate(line):
            loc = x + y*1j
            if loc in bounds:
                out += char
            elif loc in known_inside:
                out += "I"
            elif loc in known_outside:
                out += "O"
            else:
                out += char
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
