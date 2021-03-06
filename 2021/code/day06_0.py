"""https://adventofcode.com/2021/day/6"""
import logging

import boilerplate as bp

logging.basicConfig(level=logging.WARN)

DATA_PATH = bp.get_data_path()
TEST_PATH = bp.get_test_path()


def load_data(path: str) -> list:
    """Load data from file"""
    with open(path, "r") as f:
        return list(map(int, f.read().split(",")))


def start(fishes: list) -> list:
    """Count the number of fishes with each timer value"""
    # Initialize the dictionary
    count = {}
    for fish in range(9):
        count[fish] = fishes.count(fish)
    return count


def step(count: dict) -> dict:
    """Step the timer of each fish"""
    new_count = count.copy()
    for time, fish_number in count.items():
        if time == 0:
            new_count[8] = new_count.get(8, 0) + fish_number
            new_count[6] = new_count.get(6, 0) + fish_number
            new_count[0] = new_count.get(0, 0) - fish_number
        else:
            new_count[time - 1] = new_count.get(time - 1, 0) + fish_number
            new_count[time] = new_count.get(time, 0) - fish_number

    return new_count


def total_fish(count: dict) -> int:
    """Count the total number of fish"""
    return sum(count.values())


def test():
    data = load_data(TEST_PATH)
    count = start(data)
    for _ in range(80):
        count = step(count)
    assert total_fish(count) == 5934


def main():
    data = load_data(DATA_PATH)
    count = start(data)
    for _ in range(80):
        count = step(count)
    print(total_fish(count))


if __name__ == "__main__":
    test()
    main()
