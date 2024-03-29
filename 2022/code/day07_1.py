"""https://adventofcode.com/2022/day/7"""
from day07_0 import DATA_PATH, TEST_PATH, Directory, load_data


def run(data: Directory) -> int:
    need = 30_000_000 - (70_000_000 - data.size())
    big_enough = []
    for item in data.walk():
        if isinstance(item, Directory) and need <= (size := item.size()):
            big_enough.append(size)
    return min(big_enough)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 24933642


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
