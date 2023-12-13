"""https://adventofcode.com/2023/day/13"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class Tile:

    def __init__(self, tile: str) -> None:
        self.data = tile.splitlines()
        self.height = len(self.data)
        self.width = len(self.data[0])
        self.score = self.get_score()

    def is_symmetric_about(self, idx: complex) -> bool:
        if not idx.real:
            # Imaginary represents horizontal lines
            # and therefore vertical symmetry
            return self._is_vertically_symmetric_about(idx)
        if not idx.imag:
            # Real represents vertical lines
            # and therefore horizontal symmetry
            return self._is_horizontally_symmetric_about(idx)
        raise ValueError(f"Index must be real or imaginary; got {idx}")

    def _is_horizontally_symmetric_about(self, idx: complex) -> bool:
        # Real represents vertical lines and therefore horizontal symmetry
        idx = int(idx.real)
        max_l = min(idx, self.width - idx)
        forward = [l[idx - max_l:idx] for l in self.data]
        backward = ["".join(reversed(l[idx:idx + max_l])) for l in self.data]
        return forward == backward

    def _is_vertically_symmetric_about(self, idx: complex) -> bool:
        # Imaginary represents horizontal lines and therefore vertical symmetry
        idx = int(idx.imag)
        max_l = min(idx, self.height - idx)
        forward = self.data[idx - max_l:idx]
        backward = list(reversed(self.data[idx:idx + max_l]))
        return forward == backward

    def get_score(self) -> complex:
        for j in range(1, self.height):
            # Imaginary represents horizontal lines
            # and therefore vertical symmetry
            if self.is_symmetric_about(j*1j):
                # And therefore multiplied by 100
                return 100*j

        for i in range(1, self.width):
            # Real represents vertical lines
            # and therefore horizontal symmetry
            if self.is_symmetric_about(i):
                # And therefore straight
                return i
        return 0

    def pretty_print(self) -> str:
        out = ""
        if self.score%100 != 0:  # Horizontal symmetry
            for line in self.data:
                out += line[:self.score] + "|" + line[self.score:] + "\n"
        else:  # Horizontal symmetry
            score = int(self.score/100)
            out += "\n".join(self.data[:score]) + "\n"
            out += self.width*"-" + "\n"
            out += "\n".join(self.data[score:]) + "\n"
        return out


def load_data(path: str) -> list[Tile]:
    with open(path, "r") as f:
        raw = f.read().split("\n\n")
    return [Tile(tile) for tile in raw]


def run(data: list[Tile]) -> int:
    out = 0
    for tile in data:
        # print(tile.pretty_print() + "\n")  # For debugging. And it's nice.
        out += tile.score
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 405


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
