"""https://adventofcode.com/2022/day/14"""
from day14_0 import DATA_PATH, TEST_PATH, Cave, load_data, step


def drop(cave: Cave, lowest_point: int = None) -> Cave:
    if lowest_point is None:
        lowest_point = max(i.imag for i in cave if cave[i] == "#") + 1
    p = 500 + 0j
    while p.imag < lowest_point:
        new_p = step(p, cave)
        if p == new_p:
            break
        p = new_p
    else:
        cave |= {p + i: "-" for i in [-1 + 1j, 0 + 1j, 1 + 1j]}
    return cave | {p: "o"}


def run(cave: Cave) -> int:
    sands = 0
    lowest_point = max(i.imag for i in cave) + 1
    while (500 + 0j) not in cave:
        cave = drop(cave, lowest_point)
        sands += 1
    return sands


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 93


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
