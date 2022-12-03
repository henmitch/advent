"""https://adventofcode.com/2022/day/3"""
import string
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[str]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return raw


def duplicate_in_rucksack(rucksack: list[str]) -> tuple[set[str]]:
    l = len(rucksack)//2
    return (set(rucksack[:l]) & set(rucksack[l:])).pop()


def priority(value: str) -> int:
    return string.ascii_letters.index(value) + 1


def score(data: list[str]) -> int:
    return sum(priority(duplicate_in_rucksack(rucksack)) for rucksack in data)


def test():
    data = load_data(TEST_PATH)
    assert score(data) == 157


def main():
    data = load_data(DATA_PATH)
    print(score(data))


if __name__ == "__main__":
    test()
    main()
