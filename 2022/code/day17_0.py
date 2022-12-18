"""https://adventofcode.com/2022/day/17"""
from itertools import cycle
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[str]:
    with open(path, "r") as f:
        raw = f.read()
    return list(raw.strip())


class Block:

    def __init__(self, shape: str, bottom_left: complex = 2 + 3j) -> None:
        if shape not in SHAPES:
            raise ValueError(f"Invalid shape {shape}")
        self.points = SHAPES[shape](bottom_left)
        self.shape = shape

    def __repr__(self) -> str:
        return str(self.points)

    @staticmethod
    def _minus(bottom_left: complex) -> set[complex]:
        return {bottom_left + i for i in range(4)}

    @staticmethod
    def _plus(bottom_left: complex) -> set[complex]:
        return {bottom_left + i for i in (1, 1j, 1 + 1j, 2 + 1j, 1 + 2j)}

    @staticmethod
    def _ell(bottom_left: complex) -> set[complex]:
        return {bottom_left + i for i in (0, 1, 2, 2 + 1j, 2 + 2j)}

    @staticmethod
    def _i(bottom_left: complex) -> set[complex]:
        return {bottom_left + i*1j for i in range(4)}

    @staticmethod
    def _square(bottom_left: complex) -> set[complex]:
        return {bottom_left + i for i in (0, 1, 1j, 1 + 1j)}

    def move_left(self, space: set[complex]) -> None:
        if any(val.real == 0 for val in self.points):
            return None
        if (to := {val - 1 for val in self.points}) & space:
            return None
        self.points = to

    def move_right(self, space: set[complex]) -> None:
        if any(val.real == 6 for val in self.points):
            return None
        if (to := {val + 1 for val in self.points}) & space:
            return None
        self.points = to

    def move(self, direction: str, space: set[complex]) -> bool:
        if direction == "<":
            self.move_left(space)
        elif direction == ">":
            self.move_right(space)
        else:
            raise ValueError(f"Unrecognized direction {direction}")
        return self.move_down(space)

    def move_down(self, space: set[complex]) -> bool:
        if any(val.imag == 0 for val in self.points):
            return False
        if (to := {val - 1j for val in self.points}) & space:
            return False
        self.points = to
        return True


SHAPES = {
    "-": Block._minus,
    "+": Block._plus,
    "L": Block._ell,
    "I": Block._i,
    ".": Block._square
}


def max_height(space: set[complex]) -> int:
    if not space:
        return 0
    return int(max(val.imag for val in space)) + 1


def pretty_print(space: set[complex], block: Block = None) -> str:
    if block is None:
        points = set()
    else:
        points = block.points
    out = ""
    for y in range(max_height(points | space), -1, -1):
        for x in range(8):
            if (pos := x + y*1j) in points:
                out += "@"
            elif pos in space:
                out += "#"
            else:
                out += " "
        out += "\n"
    return out[:-1]


def top_boundary(space: set[complex]) -> set[complex]:
    tallests = []
    # Find the highest point in each column
    # (Assuming it's 7 units wide)
    for x in range(7):
        tallests.append(
            max_height({point
                        for point in space if point.real == x}))
    # Take the lowest of these highest points...
    lowest_tallest = min(tallests) - 1
    # ... and limit ourselves to points that're above it
    out = {point for point in space if point.imag >= lowest_tallest}
    return out


def run(data: list[str]) -> int:
    space = set()
    data = cycle(data)
    shapes = cycle(SHAPES.keys())
    for _ in range(2022):
        block = Block(next(shapes), 2 + (max_height(space) + 3)*1j)
        while block.move(next(data), space):
            pass
        space = top_boundary(space | block.points)
    print(pretty_print(space, block))
    print(7*"-")
    return max_height(space)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 3068


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    # main()
