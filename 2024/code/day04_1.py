"""https://adventofcode.com/2024/day/4"""
import boilerplate as bp
from day04_0 import DATA_PATH, TEST_PATH
from day04_0 import Search as OldSearch
from day04_0 import pretty_print


class Search(OldSearch):

    def xmases(self, key: complex) -> list[tuple[complex, ...]]:
        if self[key] != "A":
            return []
        neighbors = [key + d for d in Search.DIAGONALS]
        if any(self.oob(neighbor) for neighbor in neighbors):
            return []
        if {self[key + 1 + 1j], self[key - 1 - 1j]} != {"M", "S"}:
            return []
        if {self[key + 1 - 1j], self[key - 1 + 1j]} != {"M", "S"}:
            return []

        return [(key, *neighbors)]


def load_data(path: str) -> Search:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return Search(raw)


def run(data: Search) -> int:
    xmases = []
    for loc, _ in data:
        xmases += data.xmases(loc)
    out = len(xmases)
    locs = [loc for xmas in xmases for loc in xmas]
    print(pretty_print(data, locs))
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 9


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
