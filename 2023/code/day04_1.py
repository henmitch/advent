"""https://adventofcode.com/2023/day/4"""
from day04_0 import DATA_PATH, TEST_PATH, Card, load_data


def run(cards: list[Card]) -> int:
    n_copies = {card.id_: 1 for card in cards}
    for card in cards:
        endpoint = min(card.id_ + card.n_matches(), len(cards)) + 1
        for id_ in range(card.id_ + 1, endpoint):
            n_copies[id_] += n_copies[card.id_]
    return sum(n_copies.values())


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 30


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
