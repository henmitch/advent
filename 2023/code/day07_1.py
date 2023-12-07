"""https://adventofcode.com/2023/day/7"""
from collections import Counter

from day07_0 import DATA_PATH, TEST_PATH, CamelHand, load_data

CARDS = ["J"] + list(map(str, range(2, 10))) + ["T", "Q", "K", "A"]


class CamelHandWithJoker(CamelHand):

    def get_type_(self) -> int:
        if "J" not in self.hand:
            return super().get_type_()
        if set(self.hand) == {"J"}:
            return 6
        counts = Counter(self.hand)
        del counts["J"]
        most_common_card = counts.most_common()[0][0]
        return CamelHand(self.hand.replace("J", most_common_card), 0).type_

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


def run(data: list[list[str, int]]) -> int:
    hands = sorted(CamelHandWithJoker(*line) for line in data)
    return sum((i + 1)*hand.bid for i, hand in enumerate(hands))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 5905


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    # test()
    main()
