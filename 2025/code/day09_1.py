"""https://adventofcode.com/2025/day/9"""
import boilerplate as bp
from day09_0 import DATA_PATH, TEST_PATH, load_data, Pair, area


def sign(x: int) -> int:
    if x < 0:
        return -1
    if x == 0:
        return 0
    return 1


def v_hat(a: Pair, b: Pair) -> Pair:
    """The (semi-)normalized vector (y, x) pointing from a to b"""
    y = sign(b[0] - a[0])
    x = sign(b[1] - a[1])
    return y, x


def run(data: list[Pair]) -> int:
    out = 0
    # Reorder data such that we're starting at a top left corner (and therefore
    # know which side is the inside).
    top = min(p[0] for p in data)
    top_left = min(filter(lambda p: p[0] == top, data), key=lambda p: p[1])
    top_left_index = data.index(top_left)
    data = data[top_left_index:] + data[:top_left_index]
    # Direction towards the inside of the shape
    # If we go up (y decreases), inside_y is down (+1)
    # If we go right (x increases), inside_x is left (-1)
    # Etc.
    # Because we're currently top left, inside is +1, +1
    inside_y = 1
    inside_x = 1
    for i, point in enumerate(data[:-2]):
        considering = [data[i - 1], data[i + 1]]
        # If the next-adjacent corners are inside, consider them
        for corner in (data[i - 2], data[i + 2]):
            if v_hat(point, corner) == (inside_y, inside_x):
                considering.append(corner)
        print(point, len(considering))
        out = max(out, max(area(point, corner) for corner in considering))

        # Update our insides
        next_ = data[i + 1]
        delta_y, delta_x = v_hat(next_, point)
        if delta_y:
            inside_y = -delta_y
        if delta_x:
            inside_x = -delta_x

    return out


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
