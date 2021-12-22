"""https://adventofcode.com/2021/day/21"""
import math
import itertools
from typing import Dict, Tuple
from day21_0 import load_data, TEST_PATH, DATA_PATH

State = Tuple[Tuple[int, int], Tuple[int, int], int]
Cache = Dict[State, Tuple[int, int]]

# Some of the games will end up in positions that we've seen before. We can
# cache those positions' results to save time. After all, there are only
# 20*20*10*10*2 = 80,000 possible positions, so we can afford to cache them.
#     The above number comes from the number of scores for player 1 times the
#     number of possible scores for player 2 times the number of possible
#     positions for player 1 times the number of possible positions for player
#     2 times the number of possible next players.

# Start with both players having 20 points, at each position. Find the number
# each wins, a dict with 200 entries:
#     {((loc1, score1), (loc2, score2), next_player): (wins1, wins2)}
# Then, go to 19, do the same. Then, go to 18, etc. Once we get to 17, we'll
# start to be able to actually use the cache.


def add(t1: Tuple[int, int], t2: Tuple[int, int]) -> Tuple[int, int]:
    """Just a convenience function to add two tuples piecewise."""
    return t1[0] + t2[0], t1[1] + t2[1]


def mult(x: int, t: Tuple[int, int]) -> Tuple[int, int]:
    """Multiply a tuple by an integer."""
    return x*t[0], x*t[1]


def update_player(position: int, score: int, step: int) -> Tuple[int, int]:
    new_position = math.ceil((position + step - 0.1)%10)
    return new_position, score + new_position


def combos() -> State:
    for p1_score, p2_score in itertools.product(range(20, -1, -1),
                                                range(20, -1, -1)):
        for p1_position, p2_position in itertools.product(
                range(1, 11), range(1, 11)):
            for next_ in [0, 1]:
                yield ((p1_position, p1_score), (p2_position, p2_score), next_)


def update(cache: Cache, state: State, depth: int = 0) -> dict:
    # The number of ways each step size can occur
    if state in cache:
        return cache
    ways = {
        3: 1,  # 111
        4: 3,  # 112, 121, 211
        5: 6,  # 113, 122, 131, 212, 221, 311
        6: 7,  # 123, 132, 213, 222, 231, 312, 321
        7: 6,  # 133, 223, 232, 313, 323, 331
        8: 3,  # 233, 323, 332
        9: 1,  # 333
    }
    wins = (0, 0)
    for step, num in ways.items():
        next_ = state[-1]
        # Lists are mutable, tuples aren't.
        key = list(state)
        # We check to see if this move will make player number next_ win.
        to_update = key[next_]
        updated_player = update_player(*to_update, step)
        if updated_player[1] >= 21:
            # If it does, we add that to the win tally
            tmp = [0, 0]
            tmp[next_] = ways[step]
            wins = add(wins, tuple(tmp))
            continue
        # Now we check the cache to see if the next step is already there.
        # Everything SHOULD be in there.
        key[next_] = updated_player
        key[-1] = 1 - next_
        key = tuple(key)
        if key not in cache:
            cache = update(cache, key, depth=depth + 1)
        wins = add(wins, mult(num, cache[key]))
    cache[state] = add(cache.get(state, (0, 0)), wins)
    return cache


def fill_cache(cache: Cache) -> dict:
    for state in combos():
        cache = update(cache, state)
    return cache


def n_wins(starts: Tuple[int, int]) -> Tuple[int, int]:
    cache = fill_cache({})
    return cache[((starts[0], 0), (starts[1], 0), 0)]


def test():
    data = load_data(TEST_PATH)
    assert max(n_wins(data)) == 444356092776315


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(max(n_wins(data)))
