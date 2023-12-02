"""https://adventofcode.com/2023/day/2"""
from functools import reduce
from operator import mul

from day02_0 import DATA_PATH, TEST_PATH, Game, load_data


def find_max(game: Game) -> dict[str, int]:
    _, *matches = game
    maxes = {"red": 0, "blue": 0, "green": 0}
    for match in matches:
        for color, number in match:
            maxes[color] = max(maxes[color], number)
    return maxes


def power(game: Game) -> int:
    maxes = find_max(game)
    return reduce(mul, maxes.values())


def run(data: list[Game]) -> int:
    return sum(map(power, data))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 2286


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
