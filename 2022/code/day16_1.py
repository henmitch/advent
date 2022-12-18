"""https://adventofcode.com/2022/day/16"""
from itertools import combinations

import boilerplate as bp
from day16_0 import DATA_PATH, TEST_PATH, Cave, find_path, load_data


def find_path_pair(data: dict[str, Cave], duration: int = 26) -> int:
    # All the non-zero caves (plus AA)
    nonzero = [cave for cave in data.values() if cave.rate > 0]
    out = 0
    n = 0
    # All the possible ways to divide the nonzero caves in two
    for i in range(len(nonzero)):
        for combo in combinations(nonzero, i):
            n += 1
            if not n%100:
                print(n)
            mine, elephants = combo, list(set(nonzero) - set(combo))
            my_score = find_path(data, duration, elephants)
            elephants_score = find_path(data, duration, mine)
            out = max(out, my_score + elephants_score)
    return out


def test():
    data = load_data(TEST_PATH)
    assert find_path_pair(data) == 1707


def main():
    data = load_data(DATA_PATH)
    print(find_path_pair(data))


if __name__ == "__main__":
    # test()
    main()
