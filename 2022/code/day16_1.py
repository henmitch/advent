"""https://adventofcode.com/2022/day/16"""
from itertools import permutations

import boilerplate as bp
from day16_0 import (DATA_PATH, TEST_PATH, Cave, find_path,
                     load_data, shortest_distances)


def find_path_pair(
    data: dict[str, Cave],
    duration: int = 26
) -> tuple[dict[tuple[Cave, ...], tuple[int, int, int]], list[Cave]]:
    # All the non-zero caves (plus AA)
    nonzero = [cave for cave in data.values() if cave.rate > 0] + [data["AA"]]
    # All the possible ways to divide the nonzero caves in half
    out = 0
    my_seen = []
    elephants_seen = []
    for permutation in permutations(nonzero):
        for i in range(len(nonzero)):
            mine, elephants = permutation[:i], permutation[i:]
            # To remove redundancy; I'm too tired to know if this is helpful
            if set(mine) in my_seen or set(elephants) in elephants_seen:
                continue
            my_seen.append(set(mine))
            elephants_seen.append(set(elephants))
            my_d, my_path = find_path(data, duration, elephants)
            elephants_d, elephants_path = find_path(data, duration, mine)
            out = max(out, my_d[my_path][2] + elephants_d[elephants_path][2])
    return out


def test():
    data = load_data(TEST_PATH)
    assert find_path_pair(data) == 1707
    print("Passed!")


def main():
    data = load_data(DATA_PATH)
    print(find_path_pair(data))


if __name__ == "__main__":
    test()
    main()
