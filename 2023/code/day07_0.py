"""https://adventofcode.com/2023/day/7"""
from collections import Counter

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

CARDS = list(map(str, range(2, 10))) + ["T", "J", "Q", "K", "A"]
HAND_VALUES = [
    [1, 1, 1, 1, 1],  # High card: 0
    [1, 1, 1, 2],  # One pair: 1
    [1, 2, 2],  # Two pairs: 2
    [1, 1, 3],  # Three of a kind: 3
    [2, 3],  # Full house: 4
    [1, 4],  # Four of a kind: 5
    [5]  # Five of a kind: 6
]


def load_data(path: str) -> list[str, int]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    splitted = list(map(lambda x: x.split(), raw))
    return [(hand, int(bid)) for hand, bid in splitted]


class CamelHand:

    def __init__(self, hand: str, bid: int) -> None:
        self.hand = hand
        self.bid = bid
        self.type_ = self.get_type_()

    def __repr__(self) -> str:
        return f"('{self.hand}', {self.bid})"

    def __eq__(self, other) -> bool:
        return self.hand == other.hand

    def __lt__(self, other) -> bool:
        if self.type_ < other.type_:
            return True
        if self.type_ > other.type_:
            return False
        for mine, theirs in zip(self.hand, other.hand):
            if CARDS.index(mine) < CARDS.index(theirs):
                return True
            if CARDS.index(mine) > CARDS.index(theirs):
                return False
        return False

    def get_type_(self) -> int:
        counts = sorted(Counter(self.hand).values())
        return HAND_VALUES.index(counts)


def run(data: list[list[str, int]]) -> int:
    hands = sorted(CamelHand(*line) for line in data)
    return sum((i + 1)*hand.bid for i, hand in enumerate(hands))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 6440


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
