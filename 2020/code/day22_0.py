"""https://adventofcode.com/2020/day/22"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[list[int], list[int]]:
    with open(path, "r") as f:
        raw = f.read().split("\n\n")

    return ([int(card) for card in deck.splitlines()[1:]] for deck in raw)


def play_round(d1: list, d2: list) -> tuple[list[int], list[int]]:
    if not d1 or not d2:
        return d1, d2

    if d1[0] > d2[0]:
        return d1[1:] + [d1[0], d2[0]], d2[1:]
    else:
        return d1[1:], d2[1:] + [d2[0], d1[0]]


def score(deck: list) -> int:
    out = 0
    for i, card in enumerate(deck[::-1], start=1):
        out += i*card
    return out


def play(d1: list[int], d2: list[int]) -> int:
    while d1 and d2:
        d1, d2 = play_round(d1, d2)
    return max(score(d1), score(d2))


def test():
    d1, d2 = load_data(TEST_PATH)
    assert play(d1, d2) == 306


def main():
    d1, d2 = load_data(DATA_PATH)
    print(play(d1, d2))


if __name__ == "__main__":
    test()
    main()
