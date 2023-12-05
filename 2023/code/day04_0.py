"""https://adventofcode.com/2023/day/4"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def parse(line: str) -> tuple[int, list[int], list[int]]:
    id_, all_nums = line.split(": ")
    wins, nums = all_nums.split(" | ")
    id_ = int(id_.split()[-1])
    wins = list(map(int, wins.split()))
    nums = list(map(int, nums.split()))
    return id_, wins, nums


class Card:

    def __init__(self, id_: int, wins: list[int], nums: list[int]) -> None:
        self.id_ = id_
        self.wins = wins
        self.nums = nums

    def n_matches(self):
        return len(set(self.wins) & set(self.nums))

    def score(self):
        if not (n := self.n_matches()):
            return 0
        return 2**(n - 1)


def load_data(path: str) -> list[Card]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return [Card(*parse(line)) for line in raw]


def run(data: list[Card]) -> int:
    return sum(card.score() for card in data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 13


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
