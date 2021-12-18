"""https://adventofcode.com/2021/day/7"""
import logging

import boilerplate as bp

logging.basicConfig(level=logging.INFO)

DATA_PATH = bp.get_data_path()
TEST_PATH = bp.get_test_path()


def load_data(path: str) -> list:
    """Load data from file"""
    with open(path, "r") as f:
        return list(map(int, f.read().split(",")))


def total_distance(data: list, base: int) -> int:
    """Calculate total distance"""
    return int(sum((abs(x - base))*(1 + abs(x - base))/2 for x in data))


def optimize(data: list) -> int:
    """Optimize the data"""
    base = 0
    while True:
        if total_distance(data, base) > total_distance(data, base + 1):
            base += 1
        else:
            break
    return base


def fuel(data: list) -> int:
    """Main function"""
    return total_distance(data, optimize(data))


def test():
    """Test the solution"""
    data = load_data(TEST_PATH)
    assert fuel(data) == 168


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(fuel(data))
