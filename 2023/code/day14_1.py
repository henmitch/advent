"""https://adventofcode.com/2023/day/14"""
from day14_0 import DATA_PATH, TEST_PATH, Array, Platform

N_TIMES = 1_000_000_000


class TiltablePlatform(Platform):

    def __init__(self, drawing: str) -> None:
        super().__init__(drawing)
        locations = self.get_locations()
        self.squares = locations["#"]
        self.rounds = locations["O"]

    def tilt(self, direction: str) -> None:
        if direction == "N":
            spaces_north = self.find_spaces_north()
            self.rounds = {r - spaces_north[r]*1j for r in self.rounds}

        if direction == "S":
            spaces_south = self.find_spaces_south()
            self.rounds = {r + spaces_south[r]*1j for r in self.rounds}

        if direction == "E":
            spaces_east = self.find_spaces_east()
            self.rounds = {r + spaces_east[r] for r in self.rounds}

        if direction == "W":
            spaces_west = self.find_spaces_west()
            self.rounds = {r - spaces_west[r] for r in self.rounds}

    def _how_much_to_change_to(self, val: int, loc: complex) -> int:
        if loc in self.squares:
            return 0
        if loc in self.rounds:
            return val
        return val + 1

    def _make_mask(self) -> Array:
        return Array([[0 for _ in range(self.width)]
                      for _ in range(self.height)])

    def _make_row_mask(self) -> list[int]:
        return [0 for _ in range(self.width)]

    def _make_column_mask(self) -> list[int]:
        return [0 for _ in range(self.height)]

    def find_spaces_north(self) -> Array:
        spaces_north = self._make_mask()
        tracking = self._make_row_mask()
        for y in range(1, self.height):
            for x in range(self.width):
                loc = complex(x, y)
                above = loc - 1j
                tracking[x] = self._how_much_to_change_to(tracking[x], above)
                spaces_north[loc] = tracking[x]
        return spaces_north

    def find_spaces_south(self) -> Array:
        spaces_south = self._make_mask()
        tracking = self._make_row_mask()
        for y in range(self.height - 2, -1, -1):
            for x in range(self.width):
                loc = complex(x, y)
                below = loc + 1j
                tracking[x] = self._how_much_to_change_to(tracking[x], below)
                spaces_south[loc] = tracking[x]
        return spaces_south

    def find_spaces_east(self) -> Array:
        spaces_east = self._make_mask()
        tracking = self._make_column_mask()
        for x in range(self.width - 2, -1, -1):
            for y in range(self.height):
                loc = complex(x, y)
                right = loc + 1
                tracking[y] = self._how_much_to_change_to(tracking[y], right)
                spaces_east[loc] = tracking[y]
        return spaces_east

    def find_spaces_west(self) -> Array:
        spaces_west = self._make_mask()
        tracking = self._make_column_mask()
        for x in range(1, self.width):
            for y in range(self.height):
                loc = complex(x, y)
                left = loc - 1
                tracking[y] = self._how_much_to_change_to(tracking[y], left)
                spaces_west[loc] = tracking[y]
        return spaces_west

    def get_load(self) -> int:
        out = 0
        for round_ in self.rounds:
            out += self.height - int(round_.imag)
        return out

    def pretty_print(self) -> str:
        out = Array([["." for _ in range(self.width)]
                     for _ in range(self.height)])
        for round_ in self.rounds:
            out[round_] = "O"
        for square in self.squares:
            out[square] = "#"
        return "\n".join("".join(line) for line in out)


def load_data(path: str) -> TiltablePlatform:
    with open(path, "r") as f:
        raw = f.read()
    return TiltablePlatform(raw)


def find_last_arrangement(platform: TiltablePlatform, n: int = N_TIMES) -> int:
    step = 0
    seen = [platform.rounds]
    while True:
        step += 1
        for direction in "NWSE":
            platform.tilt(direction)
        if platform.rounds in seen:
            break
        seen.append(platform.rounds)
    initial = seen.index(platform.rounds)
    period = step - initial
    n_need = (n - initial)%period
    platform.rounds = seen[initial + n_need]
    return platform.get_load()


def run(data: TiltablePlatform) -> int:
    return find_last_arrangement(data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 64


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
