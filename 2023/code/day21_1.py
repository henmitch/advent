"""https://adventofcode.com/2023/day/21"""
# Some things potentially worth noting:
#  - Both the example and input data have no # on their edges
#  - The number of steps to take is 5*11*481843: suspiciously few factors
#  - In the real input, S has a straight shot to the edges
#  - S is dead-center in the maps
#    - Because of the above two facts, the quickest way to any other instance
#      of the map will be either to the near corner or to the middle of the
#      near edge.
#    - Unfortunately, this makes the examples not all that helpful.
from collections import UserList
from functools import cache
from typing import Iterator

from day21_0 import DATA_PATH


class Garden(UserList):

    def __init__(self, data: list[str]) -> None:
        if not data:
            self.data = [[]]
        self.height = len(data)
        self.width = len(data[0])
        super().__init__(data)
        self._hash = hash(str(self))
        self.start = self._get_start()
        self._b = complex(0, self.height - 1)
        self._r = complex(self.width - 1, 0)

    def __getitem__(self, loc: complex) -> str:
        x, y = int(loc.real), int(loc.imag)
        return self.data[y%self.height][x%self.width]

    def __iter__(self) -> Iterator:
        return self.data.__iter__()

    def __hash__(self) -> int:
        return self._hash

    def _get_start(self) -> complex:
        y = ["S" in row for row in self.data].index(True)
        x = self.data[y].index("S")
        return complex(x, y)

    @cache  # pylint: disable=method-cache-max-size-none
    def cardinal_neighbors(self, loc: complex) -> set[complex]:
        return {loc + d for d in [1, 1j, -1, -1j] if self[loc + d] != "#"}

    @cache  # pylint: disable=method-cache-max-size-none
    def cardinal_neighbors_in_bounds(self, loc: complex) -> set[complex]:
        return {n for n in self.cardinal_neighbors(loc) if not self.oob(n)}

    def oob(self, loc: complex) -> bool:
        return (loc.real < 0 or loc.imag < 0 or loc.real >= self.width
                or loc.imag >= self.height)

    @cache  # pylint: disable=method-cache-max-size-none
    def accessible_by_oddness(self, a: complex, oddness: bool) -> set[complex]:
        out = set()
        seen = set()
        to_visit = {(0, a)}
        while to_visit:
            d, loc = to_visit.pop()
            seen.add((loc, d%2))
            if d%2 == oddness:  # oddness is True if want odd, False if even
                out.add(loc)
            for neighbor in self.cardinal_neighbors_in_bounds(loc):
                if (neighbor, (d + 1)%2) in seen:
                    continue
                if self[neighbor] != "#":
                    to_visit.add((d + 1, neighbor))
        return out

    def radius(self, steps: int) -> int:
        return max(1, steps - self.start.real)//self.width + 1

    def pretty_print(self, points: set[complex] = None) -> str:
        out = ""
        min_x, max_x = 0, self.width - 1
        min_y, max_y = 0, self.height - 1
        for point in points:
            min_x = min(min_x, point.real)
            max_x = max(max_x, point.real)
            min_y = min(min_y, point.imag)
            max_y = max(max_y, point.imag)
        min_x, max_x = int(min_x), int(max_x)
        min_y, max_y = int(min_y), int(max_y)
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                loc = complex(x, y)
                if loc in points:
                    out += "O" if loc != self.start else "X"
                else:
                    out += self[loc]
            out += "\n"
        return out.strip()

    def available_spots_within(self, steps: int) -> int:
        # Odd number of steps, so the center square can access points an odd
        # number of steps away.
        oddness = steps%2
        access = len(self.accessible_by_oddness(self.start, oddness))
        inaccess = len(self.accessible_by_oddness(self.start, not oddness))
        r = self.radius(steps)
        # Because the radius (minus the center) is even, the last *full* block
        # on each row is going to be the opposite block as the middle
        from_whole_blocks = (r**2)*access + ((r - 1)**2)*inaccess
        # Mercifully, the radius is exactly 202300 full instances of the map,
        # so there's no remainder.
        # However, each non-center row is capped with a corner map on either
        # end. This corner map is of the opposite oddness as the center.
        from_corners = (r - 1)*(len(self.top_left_available(not oddness)) +
                                len(self.top_right_available(not oddness)) +
                                len(self.bottom_right_available(not oddness)) +
                                len(self.bottom_left_available(not oddness)))
        # We also lop off the outer corner from each of the outermost blocks
        # on each line
        lopped_off = r*(len(self.bottom_left_available(oddness)) +
                        len(self.bottom_right_available(oddness)) +
                        len(self.top_right_available(oddness)) +
                        len(self.top_left_available(oddness)))
        return int(from_whole_blocks + from_corners - lopped_off)

    def bottom_left_available(self, oddness: bool) -> set[complex]:
        all_ = self.accessible_by_oddness(self._b, oddness)
        return {
            p
            for p in all_
            if p.real - self.start.real < p.imag - self._b.imag
        }

    def top_left_available(self, oddness: bool) -> set[complex]:
        all_ = self.accessible_by_oddness(0j, oddness)
        return {p for p in all_ if p.real < self.start.imag - p.imag}

    def bottom_right_available(self, oddness: bool) -> set[complex]:
        all_ = self.accessible_by_oddness(self._r + self._b, oddness)
        return {
            p
            for p in all_
            if p.real - self._r.real > self.start.imag - p.imag
        }

    def top_right_available(self, oddness: bool) -> set[complex]:
        all_ = self.accessible_by_oddness(self._r, oddness)
        return {p for p in all_ if p.real - self.start.real > p.imag}


def load_data(path: str) -> Garden:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return Garden(raw)


def run(data: Garden, steps: int = 26_501_365) -> int:
    return data.available_spots_within(steps)


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    main()
