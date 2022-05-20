"""https://adventofcode.com/2019/day/1"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[int]:
    with open(path, "r") as f:
        return tuple(int(i) for i in f.readlines())


def fuel(mass: int) -> int:
    return int(mass/3) - 2


def total_fuel(masses: tuple[int, ...]) -> int:
    return sum(fuel(mass) for mass in masses)


def test():
    data = load_data(TEST_PATH)
    assert total_fuel(data) == 34241


def main():
    data = load_data(DATA_PATH)
    print(total_fuel(data))


if __name__ == "__main__":
    test()
    main()
