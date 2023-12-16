"""https://adventofcode.com/2023/day/16"""
from day16_0 import (DATA_PATH, TEST_PATH, Array, Pair, count_points,
                     find_all_next_beams, load_data, walk)


def starts(data: Array) -> list[Pair]:
    out = []
    # Top and bottom edges
    for x in range(data.width):
        out.append((x, 1j))
        out.append((x + (data.height - 1)*1j, -1j))
    # Sides
    for y in range(data.width):
        out.append((y*1j, 1))
        out.append((data.width - 1 + y*1j, -1))
    return out


def run(data: Array) -> int:
    next_beams = find_all_next_beams(data)
    return max(count_points(walk(next_beams, start)) for start in starts(data))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 51


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
