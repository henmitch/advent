"""https://adventofcode.com/2022/day/12"""
from functools import cache
from itertools import permutations
from string import ascii_lowercase
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

VALUES = ascii_lowercase


def _coordinates(data: str, value: str, width: int) -> tuple[int, int]:
    idx = data.index(value)
    y, x = divmod(idx, width + 1)
    return x, y


class ElevationMap:

    def __init__(self, data: str) -> None:
        self.data = list(map(list, data.splitlines()))
        self.width = len(self.data[0])
        self.height = len(self.data)

        self.s = _coordinates(data, "S", self.width)
        self.e = _coordinates(data, "E", self.width)

        self.data[self.s[1]][self.s[0]] = "a"
        self.data[self.e[1]][self.e[0]] = "z"

    def value(self, x: int, y: int) -> str:
        return self.data[y][x]

    @cache
    def elevation(self, x: int, y: int) -> int:
        return VALUES.index(self.value(x, y))

    @cache
    def allowed_steps(self, x: int, y: int) -> list[tuple[int, int]]:
        out = []
        v = self.elevation(x, y)
        for add_x, add_y in permutations([-1, 0, 1], 2):
            # Remove diagonals and staying put
            if abs(add_x) == abs(add_y):
                continue
            new_x, new_y = x + add_x, y + add_y
            if (new_x < 0 or new_y < 0 or new_x >= self.width
                    or new_y >= self.height):
                continue
            if self.elevation(new_x, new_y) <= v + 1:
                out.append((new_x, new_y))
        return out

    @cache
    def cost(self, x: int, y: int, w: float = 1.0) -> int:
        return abs(self.e[0] - x) + abs(self.e[1] - y) - w*self.elevation(x, y)

    def get_path_length(self, *starts: tuple[int, int]) -> int:
        # A-star to make it more likely to find minimal path
        if not starts:
            starts = (self.s,)
        to_review = set(starts)
        so_far = {start: 0 for start in starts}
        est_remain = {start: self.cost(*start) for start in starts}

        while to_review:
            current = min(to_review, key=lambda p: so_far[p] + est_remain[p])
            if current == self.e:
                return so_far[current]

            to_review.remove(current)

            for adj in self.allowed_steps(*current):
                if adj not in so_far or so_far[current] + 1 < so_far[adj]:
                    so_far[adj] = so_far[current] + 1
                    est_remain[adj] = self.cost(*adj)
                    to_review.add(adj)

        return self.width*self.height + 1


def run(data: ElevationMap) -> int:
    return data.get_path_length()


def load_data(path: str) -> ElevationMap:
    with open(path, "r") as f:
        raw = f.read()
    return ElevationMap(raw)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 31


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
