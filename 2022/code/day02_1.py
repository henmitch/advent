"""https://adventofcode.com/2022/day/2"""
import boilerplate as bp
from day02_0 import load_data, TEST_PATH, DATA_PATH

SCORES = {"X": 0, "Y": 3, "Z": 6}
OPTIONS = ["A", "B", "C"]


def play_hand(pair: tuple[str, str]) -> int:
    theirs, mine = pair
    out = SCORES[mine]
    # Lose
    if mine == "X":
        return out + (OPTIONS.index(theirs) - 1)%3 + 1
    # Tie
    if mine == "Y":
        return out + OPTIONS.index(theirs) + 1
    # Win
    if mine == "Z":
        return out + (OPTIONS.index(theirs) + 1)%3 + 1


def run(data: tuple[tuple[str, str], ...]) -> int:
    return sum(play_hand(pair) for pair in data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 12


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
