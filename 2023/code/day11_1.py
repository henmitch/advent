"""https://adventofcode.com/2023/day/11"""
from day11_0 import DATA_PATH, TEST_PATH, StarMap, between, load_data, manhattan


class FlexibleStarMap(StarMap):

    def __init__(self, data: list[str], size: int = 2) -> None:
        self.size = size
        super().__init__(data)

    def expanded_difference(self, a: complex, b: complex) -> int:
        raw = manhattan(a, b)
        expansion = 0
        for blank in self.blanks:
            if between(blank.real, (a.real, b.real)):
                expansion += self.size - 1
            if between(blank.imag, (a.imag, b.imag)):
                expansion += self.size - 1
        return raw + expansion


def run(data: list[str], size: int = 1_000_000) -> int:
    stars = FlexibleStarMap(data, size)
    distances = stars.all_distances()
    return sum(distances)


def test():
    data = load_data(TEST_PATH)
    assert run(data, 10) == 1030
    assert run(data, 100) == 8410


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
