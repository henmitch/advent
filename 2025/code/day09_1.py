"""https://adventofcode.com/2025/day/9"""
import boilerplate as bp
from day09_0 import DATA_PATH, TEST_PATH, load_data, Pair, area


def find_adjacents(a: Pair, data: list[Pair]) -> tuple[Pair, Pair]:
    horiz = [p for p in data if p != a and p[1] == a[1]]
    verti = [p for p in data if p != a and p[0] == a[0]]
    assert len(horiz) == 1
    assert len(verti) == 1

    return horiz[0], verti[0]


def find_largest_rectangle(a: Pair, data: list[Pair]) -> tuple[Pair, Pair]:
    # The next corners over
    horiz, verti = find_adjacents(a, data)
    # Potential opposite corners
    potentials = set(find_adjacents(horiz, data) + find_adjacents(verti, data))
    finalists = {horiz, verti}  # Actual, final candidate opposite corners
    # Eliminating potentials that aren't within the bounds
    for p in potentials:
        if p == a:
            continue
        # Too far vertically
        if p[1] == verti[1] and abs(p[0] - a[0]) > abs(horiz[0] - a[0]):
            continue
        # Too far horizontally
        if p[0] == horiz[0] and abs(p[1] - a[1]) > abs(verti[1] - a[1]):
            continue

        finalists.add(p)

    print(a, finalists, max(finalists, key=lambda x: area(a, x)))
    return max(finalists, key=lambda x: area(a, x))


def run(data: list[Pair]) -> int:
    return max(area(p, find_largest_rectangle(p, data)) for p in data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 24


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
