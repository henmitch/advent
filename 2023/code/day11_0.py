"""https://adventofcode.com/2023/day/11"""
import itertools

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def manhattan(a: complex, b: complex) -> int:
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def between(a: int, pair: tuple[int]) -> bool:
    left, right = pair
    return left < a < right or left > a > right


class StarMap:

    def __init__(self, data: list[str]) -> None:
        self.data = data
        self.height = len(data)
        self.width = len(data)
        self.blanks = StarMap._find_blanks(data)
        self.stars = self.find_stars()

    def __getitem__(self, loc: complex) -> str:
        try:
            return self.data[int(loc.imag)][int(loc.real)]
        except IndexError as e:
            raise IndexError(f"Invalid index {loc}") from e

    @staticmethod
    def _find_blanks(data: list[str]) -> list[complex]:
        out = []
        for y, row in enumerate(data):
            if set(row) == {"."}:
                out.append(y*1j)

        for x, col in enumerate(zip(*data)):
            if set(col) == {"."}:
                out.append(x)
        return out

    def all_points(self) -> itertools.product:
        return itertools.product(range(self.width), range(self.height))

    def find_stars(self) -> list[complex]:
        out = []
        for x, y in self.all_points():
            loc = complex(x, y)
            if self[loc] == "#":
                out.append(loc)
        return out

    def expanded_difference(self, a: complex, b: complex) -> int:
        raw = manhattan(a, b)
        expansion = 0
        for blank in self.blanks:
            if between(blank.real, (a.real, b.real)):
                expansion += 1
            if between(blank.imag, (a.imag, b.imag)):
                expansion += 1
        return raw + expansion

    def all_distances(self) -> list[int]:
        out = []
        for a, b in itertools.combinations(self.stars, 2):
            out.append(self.expanded_difference(a, b))
        return out


def run(data: list[str]) -> int:
    stars = StarMap(data)
    distances = stars.all_distances()
    return sum(distances)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 374


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
