"""https://adventofcode.com/2023/day/13"""
from day13_0 import DATA_PATH, TEST_PATH, Tile


class SmudgedTile(Tile):

    def __init__(self, tile: str) -> None:
        super().__init__(tile)
        self.smudge_score = self.get_smudge_score()

    def has_smudge(self, idx: complex) -> bool:
        if not idx.real:
            # Imaginary represents horizontal lines
            # and therefore vertical symmetry
            return self._has_smudge_for_vertical_symmetry(idx)
        if not idx.imag:
            # Real represents vertical lines
            # and therefore horizontal symmetry
            return self._has_smudge_for_horizontal_symmetry(idx)
        raise ValueError(f"Index must be real or imaginary; got {idx}")

    def _has_smudge_for_vertical_symmetry(self, idx: complex) -> bool:
        # Imaginary represents horizontal lines and therefore vertical symmetry
        potentially_found = False
        idx = int(idx.imag)
        max_l = min(idx, self.height - idx)
        forward = self.data[idx - max_l:idx]
        backward = list(reversed(self.data[idx:idx + max_l]))
        for f, b in zip("".join(forward), "".join(backward)):
            if f == b:
                continue
            # If we already maybe found one, give up
            if potentially_found:
                return False
            potentially_found = True
        return potentially_found

    def _has_smudge_for_horizontal_symmetry(self, idx: complex) -> bool:
        # Real represents vertical lines and therefore horizontal symmetry
        potentially_found = False
        idx = int(idx.real)
        max_l = min(idx, self.width - idx)
        forward = [l[idx - max_l:idx] for l in self.data]
        backward = ["".join(reversed(l[idx:idx + max_l])) for l in self.data]
        for f, b in zip(forward, backward):
            if f == b:
                continue
            # If we already maybe found one, give up
            if potentially_found:
                return False
            potentially_found = True
        return potentially_found

    def get_smudge_score(self) -> complex:
        for j in range(1, self.height):
            # Imaginary represents horizontal lines
            # and therefore vertical symmetry
            if self.has_smudge(j*1j):
                # And therefore multiplied by 100
                return 100*j

        for i in range(1, self.width):
            # Real represents vertical lines
            # and therefore horizontal symmetry
            if self.has_smudge(i):
                # And therefore straight
                return i
        return 0


def load_data(path: str) -> list[SmudgedTile]:
    with open(path, "r") as f:
        raw = f.read().split("\n\n")
    return [SmudgedTile(tile) for tile in raw]


def run(data: list[SmudgedTile]) -> int:
    return sum(tile.smudge_score for tile in data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 400


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
