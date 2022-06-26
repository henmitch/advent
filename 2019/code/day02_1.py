"""https://adventofcode.com/2019/day/2"""
from day02_0 import DATA_PATH, TEST_PATH, IntCode, load_data


def run(data: list[int], target: int) -> int:
    for noun in range(100):
        for verb in range(100):
            if IntCode(data, noun, verb).run() == target:
                return 100*noun + verb


def test():
    data = load_data(DATA_PATH)
    assert run(data, 7594646) == 1202


def main():
    data = load_data(DATA_PATH)
    print(run(data, 19690720))


if __name__ == "__main__":
    test()
    main()
