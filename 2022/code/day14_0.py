"""https://adventofcode.com/2022/day/14"""
from functools import reduce
from operator import or_

import boilerplate as bp

Cave = dict[complex, str | tuple[complex]]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def make_path(path: str) -> Cave:
    lines = list(map(pairify, (pair for pair in path.split(" -> "))))
    out = {}
    for p1, p2 in zip(lines, lines[1:]):
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2:
            y1, y2 = sorted([y1, y2])
            out |= {x1 + y*1j: "#" for y in range(y1, y2 + 1)}
        elif y1 == y2:
            x1, x2 = sorted([x1, x2])
            out |= {x + y1*1j: "#" for x in range(x1, x2 + 1)}
        else:
            raise ValueError("Line was neither horizontal nor vertical")
    return out


def load_data(path: str) -> Cave:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return reduce(or_, (make_path(p) for p in raw))


def pairify(pair: str) -> complex:
    x, y = tuple(map(int, pair.split(",")))
    return x, y


def step(p: complex, cave: Cave) -> complex:
    if p + 1j not in cave:
        return p + 1j
    if p + (-1 + 1j) not in cave:
        return p + (-1 + 1j)
    if p + (1 + 1j) not in cave:
        return p + (1 + 1j)
    return p


def drop(cave: Cave) -> Cave:
    lowest_point = max(i.imag for i in cave)
    p = 500 + 0j
    path = [p]
    while p.imag < lowest_point:
        p = step(p, cave)
        if p in path:
            path.append(p)
            break
        path.append(p)
    return cave | {p: tuple(path[:-1])}


def run(cave: Cave) -> int:
    sands = 0
    while len(set(cave.values())) == sands + 1:
        cave = drop(cave)
        sands += 1
    # Minus 1 for the one that fell off the earth, -1 for the one that followed
    return sands - 2


def pretty_print(cave: Cave) -> str:
    min_x = int(min(p.real for p in cave))
    max_x = int(max(p.real for p in cave))
    max_y = int(max(p.imag for p in cave))
    out = ""
    for y in range(max_y + 1):
        for x in range(min_x, max_x + 1):
            if (p := x + y*1j) not in cave:
                out += "."
            elif cave[p] == "#":
                out += "#"
            else:
                out += "o"
        out += "\n"
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 24


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
