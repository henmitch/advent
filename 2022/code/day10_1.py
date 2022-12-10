"""https://adventofcode.com/2022/day/10"""
from day10_0 import DATA_PATH, TEST_PATH, execute, load_data


def draw(data: list[int]) -> str:
    out = ""
    for row in range(6):
        for column in range(40):
            loc = column
            if data[row*40 + loc] in [loc - 1, loc, loc + 1]:
                out += "#"
            else:
                out += "."
        out += "\n"
    return out


def run(data: list[str]) -> str:
    return draw(execute(data))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == ("##..##..##..##..##..##..##..##..##..##..\n"
                         "###...###...###...###...###...###...###.\n"
                         "####....####....####....####....####....\n"
                         "#####.....#####.....#####.....#####.....\n"
                         "######......######......######......####\n"
                         "#######.......#######.......#######.....\n")


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
