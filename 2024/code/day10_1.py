"""https://adventofcode.com/2024/day/10"""
import boilerplate as bp
from day10_0 import DATA_PATH, TEST_PATH
from day10_0 import Grid as OldGrid


class Grid(OldGrid):

    def number_of_paths_to_nines(self, loc: complex) -> int:
        if self[loc] == 9:
            return 1
        out = 0
        for neighbor in self.neighbors(loc):
            if self[neighbor] == self[loc] + 1:
                out += self.number_of_paths_to_nines(neighbor)
        return out


def load_data(path: str) -> Grid:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return Grid([[int(x) for x in row] for row in raw])


def run(data: Grid) -> int:
    out = 0
    for loc, val in data:
        if val == 0:
            out += data.number_of_paths_to_nines(loc)
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 81


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
