"""https://adventofcode.com/2023/day/22"""
import itertools
from collections import deque
from functools import reduce
from operator import or_

from day22_0 import DATA_PATH, TEST_PATH, Brick, drop_all, load_data

Bricks = set[Brick]


def is_floating(brick: Brick, friends: Bricks) -> bool:
    if brick.is_grounded():
        return False
    for friend in friends:
        if brick.is_supported_by(friend):
            return False
    return True


def get_chain_reaction(bricks: list[Brick]) -> dict[Brick, int]:
    out: dict[Brick, Bricks] = {}
    supporters = {}
    supportees = {}
    tops = set(bricks)
    for brick, friend in itertools.combinations(bricks, 2):
        if friend.supports(brick):
            supporters[brick] = supporters.get(brick, set()) | {friend}
            supportees[friend] = supportees.get(friend, set()) | {brick}
            tops -= {friend}
        if brick.supports(friend):
            supporters[friend] = supporters.get(friend, set()) | {brick}
            supportees[brick] = supportees.get(brick, set()) | {friend}
            tops -= {brick}
    singles = reduce(or_, [v for v in supporters.values() if len(v) == 1])
    for single in singles:
        droppeds = {single}
        potential_floaters = deque(supportees[single])
        while potential_floaters:
            potential_floater = potential_floaters.popleft()
            # Check the supportees of each dropped brick
            # If all of its supporters have dropped, it drops
            if is_floating(potential_floater,
                           supporters[potential_floater] - droppeds):
                droppeds.add(potential_floater)
                if potential_floater not in supportees:
                    continue
                # Then we add everybody it's holding up to the list of
                # potential floaters
                for supportee in supportees[potential_floater]:
                    potential_floaters.append(supportee)
            # If we have no supportees (i.e., we've reached the top), we carry
            # on and leave it off the queue
            elif potential_floater not in supportees:
                continue
            # If any of the supporters might be dangling, we put it back in the
            # queue
            elif any(supportee in potential_floaters
                     for supportee in supportees[potential_floater]):
                potential_floaters.append(potential_floater)

        out[single] = droppeds - {single}
    return out


def run(data: list[Brick]) -> int:
    bricks = drop_all(data)
    return sum(len(v) for v in get_chain_reaction(bricks).values())


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 7


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
