"""https://adventofcode.com/2021/day/3"""
import os

data_dir = os.path.join(os.path.dirname(__file__), "data")
path = os.path.join(data_dir, "day03_0.txt")
with open(path, "r") as f:
    data = f.read().splitlines()


def filter_(lst: list, bit: int, n: int = 0) -> int:
    if len(lst) == 1:
        return int(lst[0], 2)
    if n >= len(lst[0]):
        raise ValueError("Invalid bit position.")

    most = int(sum(int(x[n]) for x in lst) // (len(lst) / 2))
    next_lst = [x for x in lst if not int(x[n]) == (bit ^ most)]

    return filter_(next_lst, bit, n + 1)


oxygen_rating = filter_(data, 1)
co2_rating = filter_(data, 0)

out = oxygen_rating * co2_rating
print(f"The life support rating is {out}")
