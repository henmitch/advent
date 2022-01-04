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
    seen = {i: 0 for i in range(n_rounds)}
    seen |= {starter: i + 1 for i, starter in enumerate(starters)}
    last = starters[-1]
    l = len(starters)
    for idx in range(l, n_rounds):
        last = step(last, idx, seen)
    return last


def step(last: int, idx: int, seen: Dict[int,
                                         int]) -> Tuple[Dict[int, int], int]:
    val = seen[last]
    seen[last] = idx
    if val:
        return idx - val
    else:
        return 0


def test():
    data = load_data(TEST_PATH)
    assert play_game(data, 30_000_000) == 175594
    assert play_game((1, 3, 2), 30_000_000) == 2578
    assert play_game((2, 1, 3), 30_000_000) == 3544142
    assert play_game((1, 2, 3), 30_000_000) == 261214
    assert play_game((2, 3, 1), 30_000_000) == 6895259
    assert play_game((3, 2, 1), 30_000_000) == 18
    assert play_game((3, 1, 2), 30_000_000) == 362


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(play_game(data, 30_000_000))
