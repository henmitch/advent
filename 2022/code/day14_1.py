"""https://adventofcode.com/2022/day/14"""
from day14_0 import DATA_PATH, TEST_PATH, Cave, load_data, step


def drop(cave: Cave) -> Cave:
    lowest_point = max(i.imag for i in cave if cave[i] == "#") + 1
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
    while (500 + 0j) not in cave:
        cave = drop(cave)
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
