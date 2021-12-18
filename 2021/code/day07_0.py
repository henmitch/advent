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


def median(data: list) -> int:
    """Calculate median of data"""
    return sorted(data)[len(data)//2]


def total_distance(data: list, base: int) -> int:
    """Calculate total distance"""
    return sum(abs(x - base) for x in data)


def fuel(data: list) -> int:
    """Calculate the total fuel used"""
    return total_distance(data, median(data))


def test():
    """Test the solution"""
    data = load_data(TEST_PATH)
    assert fuel(data) == 37


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(fuel(data))
