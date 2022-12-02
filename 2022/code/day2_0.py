"""https://adventofcode.com/2022/day/2"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

SCORES = {"X": 1, "Y": 2, "Z": 3}


def load_data(path: str) -> tuple[tuple[str, str], ...]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    out = tuple(tuple(line.split()) for line in raw)
    return out


def play_hand(pair: tuple[str, str]) -> int:
    out = SCORES[pair[1]]
    # Ties
    if pair in {("A", "X"), ("B", "Y"), ("C", "Z")}:
        return out + 3
    # I win
    if pair in {("A", "Y"), ("B", "Z"), ("C", "X")}:
        return out + 6
    return out


def run(data: tuple[tuple[str, str], ...]) -> int:
    return sum(play_hand(pair) for pair in data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 15


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
