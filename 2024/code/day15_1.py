"""https://adventofcode.com/2024/day/15"""
from itertools import cycle

import boilerplate as bp
from day15_0 import DATA_PATH, DIRECTIONS, TEST_PATH_0


class Grid:

    def __init__(self, walls: set[complex], boxes: set[complex],
                 pairs: dict[complex, complex]) -> None:
        self.walls = walls
        self.boxes = boxes
        self.pairs = pairs
        self.width = max(int(loc.real) for loc in walls | boxes) + 1
        self.height = max(int(loc.imag) for loc in walls | boxes) + 1

    def can_move(self, loc: complex, direction: complex) -> bool:
        step = loc + direction
        if step in self.walls:
            # We can't move into walls
            return False

        if loc not in self.boxes and step not in self.boxes:
            # We can move the robot into empty spaces
            return True

        if loc not in self.boxes and step in self.boxes:
            # Need to check the box we're pushing
            return self.can_move(step, direction)

        # We're moving a box
        pair = self.pairs[loc] + direction
        if pair in self.walls:
            # We can't push our partner into a wall
            # (We already checked if we would hit a wall)
            return False

        if step in self.boxes:
            if not self.can_move(step, direction):
                # If we're pushing a box that can't be moved, we can't move
                return False

        if pair in self.boxes and pair != loc:
            # Don't need to check the partner if we're pushing into it
            if not self.can_move(pair, direction):
                # If we're pushing a box that can't be moved, we can't move
                return False

        return True

    def move(self, loc: complex, direction: complex) -> complex:
        if not self.can_move(loc, direction):
            return loc
        step = loc + direction
        if step not in self.boxes:
            return step

        self.boxes.remove(step)
        self.boxes.remove(self.pairs[step])
        a = self.move(step, direction)
        b = self.move(self.pairs[step], direction)
        self.boxes.add(a)
        self.boxes.add(b)
        del self.pairs[self.pairs[step]]
        del self.pairs[step]
        self.pairs[a] = b
        self.pairs[b] = a

        return step

    def left_edges(self) -> set[complex]:
        out = set()
        for box in self.boxes:
            if box.real == min(box.real, self.pairs[box].real):
                out.add(box)
        return out

    def gps(self, loc: complex) -> int:
        return int(100*loc.imag + loc.real)

    def pretty_print(self, loc: complex) -> str:
        out = ""
        symbols = cycle("[]")
        for y in range(self.height):
            for x in range(self.width):
                pos = x + y*1j
                if pos in self.walls:
                    out += "#"
                elif pos == loc:
                    out += "@"
                elif pos in self.boxes:
                    out += next(symbols)
                else:
                    out += " "
            out += "\n"
        return out


def load_data(path: str) -> tuple[Grid, list[complex], complex]:
    with open(path, "r") as f:
        grid, instructions = f.read().split("\n\n")

    grid = grid.replace(".", "..") \
               .replace("#", "##") \
               .replace("O", "[]") \
               .replace("@", "@.")

    walls = set()
    boxes = set()
    pairs = {}
    starter = None

    for y, row in enumerate(grid.splitlines()):
        for x, char in enumerate(row):
            if char == "#":
                walls.add(x + y*1j)
            elif char == "[":
                boxes.add(x + y*1j)
                boxes.add(x + 1 + y*1j)
                pairs[x + y*1j] = x + 1 + y*1j
                pairs[x + 1 + y*1j] = x + y*1j
            elif char == "@":
                starter = x + y*1j

    if starter is None:
        raise ValueError("No starting position found")

    instructions = [DIRECTIONS[d] for d in instructions.replace("\n", "")]

    return Grid(walls, boxes, pairs), instructions, starter


def run(data: tuple[Grid, list[complex], complex]) -> int:
    grid, instructions, bot = data
    for direction in instructions:
        bot = grid.move(bot, direction)

    return sum(grid.gps(box) for box in grid.left_edges())


def test():
    data = load_data(TEST_PATH_0)
    assert run(data) == 9021


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
