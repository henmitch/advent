"""https://adventofcode.com/2023/day/17"""
import heapq
import itertools
from collections import UserList
from dataclasses import dataclass
from typing import Any, Iterator, Sequence

import boilerplate as bp

Pair = tuple[complex, complex]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

CARDINAL_DIRECTIONS = {1, -1, 1j, -1j}


@dataclass(frozen=True)
class State:
    loc: complex
    direction: complex

    def __lt__(self, other) -> bool:
        # We're defining in terms of distance from the end, so a higher
        # magnitude should be "less than" a lower magnitude
        return abs(self.loc) > abs(other.loc)


class Array(UserList):

    def __init__(self, data: Sequence[Sequence]) -> None:
        if not data:
            self.data = [[]]
        self.height = len(data)
        self.width = len(data[0])
        super().__init__(data)

    def __getitem__(self, loc: complex) -> str:
        x, y = int(loc.real), int(loc.imag)
        return self.data[y][x]

    def __setitem__(self, loc: complex, val: Any) -> None:
        x, y = int(loc.real), int(loc.imag)
        self.data[y][x] = val

    def all_points(self) -> Iterator[tuple[complex, str]]:
        for y, x in itertools.product(range(self.height), range(self.width)):
            loc = complex(x, y)
            yield loc, self[loc]

    def __iter__(self) -> Iterator:
        return self.data.__iter__()

    def oob(self, loc: complex) -> bool:
        return (loc.real < 0 or loc.imag < 0 or loc.real >= self.width
                or loc.imag >= self.height)

    def next_options(
        self, state: State,
        ls: Sequence = range(1, 4)) -> list[tuple[State, int]]:
        # Returns the ending state and the cost to get from the given to there
        out = []
        disallowed = {-state.direction, state.direction}
        for d in CARDINAL_DIRECTIONS - disallowed:
            if self.oob(state.loc + d*ls[0]):
                continue
            cost = sum(self[state.loc + l*d] for l in range(1, ls[0]))
            for length in ls:
                if not self.oob(new_loc := state.loc + length*d):
                    cost += self[new_loc]
                    out.append((State(new_loc, d), cost))
        return out

    def get_est_cost(self, loc: complex) -> int:
        d = complex(self.width - 1, self.height - 1) - loc
        return d.real + d.imag

    def walk(self, lengths: Sequence = range(1, 4)) -> list[State]:
        start = 0 + 0j
        end = complex(self.width, self.height) - (1 + 1j)
        to_check = [(0, State(start, 1)), (0, State(start, 1j))]
        heapq.heapify(to_check)
        costs = {State(start, 1): 0, State(start, 1j): 0}

        while to_check:
            _, state = heapq.heappop(to_check)
            if state.loc == end:
                return costs[state]

            for new_state, cost in self.next_options(state, lengths):
                new_loc = new_state.loc
                new_cost = costs[state] + cost
                if new_state not in costs or new_cost < costs[new_state]:
                    costs[new_state] = new_cost
                    sorter = new_cost + self.get_est_cost(new_loc)
                    heapq.heappush(to_check, (sorter, new_state))

        raise RuntimeError("Never reached endpoint")

    def sum(self, path: list[complex]) -> int:
        return sum(self[v] for v in path)


def load_data(path: str) -> Array:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return Array([[int(x) for x in line] for line in raw])


def run(data: Array) -> int:
    return data.walk()


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 102


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
