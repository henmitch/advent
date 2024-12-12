"""https://adventofcode.com/2024/day/12"""
import boilerplate as bp

TEST_PATH_0 = bp.get_test_path("0")
TEST_PATH_1 = bp.get_test_path("1")
TEST_PATH_2 = bp.get_test_path("2")
DATA_PATH = bp.get_data_path()


class Garden:

    CARDINALS = [1, 1j, -1, -1j]

    def __init__(self, plot: list[str]) -> None:
        self.plot = plot
        self.width = len(plot[0])
        self.height = len(plot)

    def __getitem__(self, key: complex) -> str:
        return self.plot[int(key.imag)][int(key.real)]

    def __iter__(self):
        for y, row in enumerate(self.plot):
            for x, cell in enumerate(row):
                yield complex(x, y), cell

    def oob(self, pos: complex) -> bool:
        return not (0 <= pos.real < self.width and 0 <= pos.imag < self.height)

    def neighbors(self, pos: complex) -> list[complex]:
        return [pos + c for c in self.CARDINALS]


def load_data(path: str) -> Garden:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return Garden(raw)


def score(a: dict[str, int], b: dict[str, int]) -> int:
    return sum(a[k]*b[k] for k in a.keys() & b.keys())


def perimeter(region: set[complex]) -> int:
    out = 0
    for pos in region:
        for d in Garden.CARDINALS:
            if pos + d not in region:
                out += 1
    return out


def run(data: Garden) -> int:
    # First, separate the data into continguous regions
    regions = {}
    for pos, cell in data:
        regions[pos] = regions.get(pos, set()) | {pos}
        for n in data.neighbors(pos):
            if data.oob(n):
                continue
            if data[n] == cell:
                regions[pos] = regions[pos] | {n} | regions.get(n, set())
                for loc in regions[pos]:
                    regions[loc] = regions[pos]

    for region, locs in regions.items():
        regions[region] = frozenset(locs)

    # Then, calculate the area and perimeter of each region
    areas = {v: len(v) for v in regions.values()}
    perimeters = {v: perimeter(v) for v in regions.values()}
    out = score(areas, perimeters)
    return out


def test():
    data_0 = load_data(TEST_PATH_0)
    assert run(data_0) == 140
    data_1 = load_data(TEST_PATH_1)
    assert run(data_1) == 772
    data_2 = load_data(TEST_PATH_2)
    assert run(data_2) == 1930


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
