"""https://adventofcode.com/2021/day/23"""
from __future__ import annotations

import copy
import heapq
from typing import List, Set, Tuple

import boilerplate as bp

Point = Tuple[int, int]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

HOME = {
    "A": ((3, 2), (3, 3)),
    "B": ((5, 2), (5, 3)),
    "C": ((7, 2), (7, 3)),
    "D": ((9, 2), (9, 3))
}
HOME_POINTS = set()
for top, bottom in HOME.values():
    HOME_POINTS.add(top)
    HOME_POINTS.add(bottom)
INBOUNDS = {(x, 1)
            for x in range(1, 12)} | {(x, y)
                                      for x in [3, 5, 7, 9] for y in [2, 3]}
RED_ZONE = {(x, 1) for x in [3, 5, 7, 9]}  # For loading and unloading only


def adjacent(coord: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """Return the coordinates of the adjacent cells to the given one."""
    x, y = coord
    return {(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)}


def parse(description: str) -> Tuple[Amphipod]:
    out: List[Amphipod] = []
    for y, line in enumerate(description):
        for x, char in enumerate(line):
            if char in "ABCD":
                out.append(Amphipod(char, (x, y)))
    for a in out:
        a.friends = set(out) - {a}
        a.set_buddy()
    return tuple(out)


def load_data(path: str) -> List[Amphipod]:
    with open(path) as f:
        return parse(f.read().splitlines())


# Amphipods will make at most 2 moves: out of their original spot, and into
# their home.


class Amphipod:
    def __init__(self, type_: str, loc: Point):
        self.type_: str = type_
        self.cost: int = 10**("ABCD".index(self.type_))
        self.home: Tuple[Point] = HOME[type_]
        self.loc: Point = loc
        self.energy: int = 0
        self.moved: bool = False
        self.friends: Set[Amphipod] = set()
        self.buddy: Amphipod = None
        self.friends_homes = HOME_POINTS - set(self.home)

    def __repr__(self) -> str:
        return f"{self.type_}{self.loc}"

    def __lt__(self, other: Amphipod) -> bool:
        return self.energy <= other.energy

    def set_buddy(self) -> None:
        for friend in self.friends:
            if friend.type_ == self.type_:
                self.buddy = friend
                break

    def is_home(self) -> bool:
        return self.loc in self.home

    def is_done(self) -> bool:
        if self.loc == self.home[1]:
            return True
        return self.is_home() and self.buddy.is_done()

    def adjacents(self) -> Set[Point]:
        return adjacent(self.loc) & INBOUNDS

    def path(self, endpoint: Point = None) -> Tuple[Point]:
        """Dijkstra search to find home or endpoint"""
        to_review = {self.loc}
        lineage = {self.loc: None}
        so_far = {self.loc: 0}

        if endpoint is None:
            if self.is_done():
                return ((self.loc), )
            if self.buddy.is_done():
                endpoint = self.home[0]
            else:
                endpoint = self.home[1]

        while to_review:
            current = min(to_review, key=lambda p: so_far[p])
            if current == endpoint:
                out = []
                while current is not None:
                    out.append(current)
                    current = lineage[current]
                return tuple(reversed(out))

            to_review.remove(current)

            for adj in adjacent(current) & INBOUNDS:
                new_cost = so_far[current] + 1
                if adj not in so_far or new_cost < so_far[adj]:
                    lineage[adj] = current
                    so_far[adj] = new_cost
                    to_review.add(adj)

    def is_blocked(self) -> bool:
        for friend in self.friends:
            if friend.blocks(self):
                if not (friend is self.buddy and self.buddy.is_done()):
                    pass
                return True
        return False

    def blocks(self, other: Amphipod) -> bool:
        return self.loc in other.path()

    def can_go_home(self) -> bool:
        if self.is_blocked():
            return False
        if self.buddy.is_done():
            return True
        if any(f.loc in self.home for f in self.friends):
            return False
        return True

    def legally_parked(self) -> bool:
        return self.loc not in RED_ZONE

    def viable_spots(self) -> Set[Point]:
        if self.is_done():
            return set()
        if self.can_go_home():
            if self.buddy.is_done():
                return {self.home[0]}
            else:
                return {self.home[1]}
        friends_spots = {f.loc for f in self.friends}

        to_explore = self.adjacents() - friends_spots
        spots = set()
        while to_explore:
            check = to_explore.pop()
            if check in friends_spots:
                continue
            spots.add(check)
            to_explore |= (adjacent(check) & INBOUNDS)
            to_explore -= spots

        spots -= ({self.loc} | RED_ZONE | self.friends_homes | friends_spots)

        # If there's someone else in our home and it's not our buddy, we can't
        # go there.
        if not self.buddy.is_home():
            spots -= set(self.home)
        if self.moved:
            return set(self.home) & spots
        return spots

    def move(self, to: Point, force: bool = False) -> bool:
        if to not in self.viable_spots():
            return False
        if to in self.home and any(f.blocks(self) for f in self.friends):
            return False

        if not force:
            self.moved = True
            self.energy += self.cost*(len(self.path(to)) - 1)
        self.loc = to
        return True


def pretty_print(amps: List[Amphipod]) -> str:
    out = [[" "]*12 for _ in range(5)]
    for amp in amps:
        out[amp.loc[1]][amp.loc[0]] = amp.type_
    return "\n".join("".join(row) for row in out)


def total_energy(amps: List[Amphipod]) -> int:
    return sum(a.energy for a in amps)


def shrink(amps: List[Amphipod]) -> str:
    return "".join(f"{a.type_}{a.loc[0]}{a.loc[1]}" for a in amps)


def all_possible_next_moves(amps: List[Amphipod]) -> List[List[Amphipod]]:
    for i, a in enumerate(amps):
        for spot in a.viable_spots():
            clone = copy.deepcopy(amps)
            a = clone[i]
            if a.move(spot):
                yield (clone, total_energy(clone))
            else:
                raise ValueError("Can't move there")
            del clone, a


def closeness(amps: List[Amphipod]) -> int:
    # Smaller is better.
    return sum(abs(a.loc[0] - a.home[0][0]) for a in amps)


def find_all_states(amps: List[Amphipod]) -> int:
    to_review = [(0, amps)]
    so_far = {shrink(amps): 0}
    # lineage = {amps: None}

    iter_count = 0
    while to_review:
        iter_count += 1
        if iter_count%1000 == 0:
            print(f"Iteration {iter_count}")
            print(f"{len(to_review)} states to review")
            print(f"{len(so_far)} states so far")
            print(pretty_print(amps))
            print()
        _, amps = heapq.heappop(to_review)
        shrunk_amps = shrink(amps)
        if all(amp.is_done() for amp in amps):
            return amps, so_far[shrunk_amps]

        for next_amps, cost in set(all_possible_next_moves(amps)):
            shrunk = shrink(next_amps)
            # Anything over 19,000 involves extra moves of D. No thanks!
            if (shrunk not in so_far
                    or cost < so_far[shrunk] and not cost > 19000):
                d = closeness(next_amps)
                so_far[shrunk] = cost
                heapq.heappush(to_review, (cost + d, next_amps))


def test():
    amps = load_data(TEST_PATH)
    t = find_all_states(amps)
    print(t)
    return t


if __name__ == "__main__":
    # t = test()
    amps = load_data(DATA_PATH)
    t = find_all_states(amps)
    print(t)
