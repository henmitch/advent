"""https://adventofcode.com/2024/day/15"""
import boilerplate as bp

TEST_PATH_0 = bp.get_test_path("0")
TEST_PATH_1 = bp.get_test_path("1")
DATA_PATH = bp.get_data_path()

DIRECTIONS = {"^": -1j, "v": 1j, "<": -1, ">": 1}


class Grid:

    def __init__(self, walls: set[complex], boxes: set[complex]) -> None:
        self.walls = walls
        self.boxes = boxes
        self.width = max(int(loc.real) for loc in walls | boxes) + 1
        self.height = max(int(loc.imag) for loc in walls | boxes) + 1

    def move(self, loc: complex, direction: complex) -> complex:
        step = loc + direction
        if step in self.walls:
            return loc
        if step in self.boxes:
            self.boxes.remove(step)
            self.boxes.add(self.move(step, direction))
        return step if step not in self.boxes else loc

    def gps(self, loc: complex) -> int:
        return int(100*loc.imag + loc.real)

    def pretty_print(self, loc: complex) -> str:
        out = ""
        for y in range(self.height):
            for x in range(self.width):
                pos = x + y*1j
                if pos in self.walls:
                    out += "#"
                elif pos == loc:
                    out += "X"
                elif pos in self.boxes:
                    out += "O"
                else:
                    out += " "
            out += "\n"
        return out


def load_data(path: str) -> tuple[Grid, list[complex], complex]:
    with open(path, "r") as f:
        grid, instructions = f.read().split("\n\n")

    walls = set()
    boxes = set()
    starter = None

    for y, row in enumerate(grid.splitlines()):
        for x, char in enumerate(row):
            if char == "#":
                walls.add(x + y*1j)
            elif char == "O":
                boxes.add(x + y*1j)
            elif char == "@":
                starter = x + y*1j

    if starter is None:
        raise ValueError("No starting position found")

    instructions = [DIRECTIONS[d] for d in instructions.replace("\n", "")]

    return Grid(walls, boxes), instructions, starter


def run(data: tuple[Grid, list[complex], complex]) -> int:
    grid, instructions, bot = data
    for direction in instructions:
        bot = grid.move(bot, direction)
    return sum(grid.gps(box) for box in grid.boxes)


def test():
    data = load_data(TEST_PATH_1)
    assert run(data) == 2028
    data = load_data(TEST_PATH_0)
    assert run(data) == 10092


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
