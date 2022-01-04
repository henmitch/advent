"""https://adventofcode.com/2020/day/15"""
from typing import Dict, Tuple
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> Tuple[int]:
    with open(path, "r") as f:
        raw = f.read().split(",")
    return tuple(map(int, raw))


def play_game(starters: Tuple[int], n_rounds: int = 2020) -> int:
    seen = {starter: i + 1 for i, starter in enumerate(starters[:-1])}
    last = starters[-1]
    l = len(starters)
    for idx in range(l, n_rounds):
        seen, last = step(last, idx, seen)
    return last


def step(last: int, idx: int, seen: Dict[int,
                                         int]) -> Tuple[Dict[int, int], int]:
    if not last in seen:
        return seen | {last: idx}, 0
    return seen | {last: idx}, idx - seen[last]


def test():
    data = (0, 3, 6)
    assert play_game(data, 10) == 0
    assert play_game(data) == 436
    assert play_game((1, 3, 2)) == 1
    assert play_game((2, 1, 3)) == 10
    assert play_game((1, 2, 3)) == 27
    assert play_game((2, 3, 1)) == 78
    assert play_game((3, 2, 1)) == 438
    assert play_game((3, 1, 2)) == 1836


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(play_game(data))
