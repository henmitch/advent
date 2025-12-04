"""https://adventofcode.com/2025/day/3"""
from boilerplate import write_answer
from day03_0 import DATA_PATH, TEST_PATH, load_data


def power_of_line(line: tuple[int, ...]) -> int:
    out = 0
    testing = line
    for i in range(11):
        m = max(testing[:-(11 - i)])
        out += m*(10**(11 - i))
        testing = testing[testing.index(m) + 1:]
    out += max(testing)
    return out


def run(data: tuple[int]) -> int:
    out = 0
    for line in data:
        out += power_of_line(line)
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 3121910778619


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
