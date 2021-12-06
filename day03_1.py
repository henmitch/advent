"""https://adventofcode.com/2021/day/3"""
import logging
import os

data_dir = os.path.join(os.path.dirname(__file__), "data")
path = os.path.join(data_dir, "day03_0.txt")
with open(path, "r") as f:
    data = f.read().splitlines()


def filter_(lst: list, bit: str, n: int = 0) -> int:
    logging.info(f"{len(lst)=} {bit=} {n=}")
    if len(lst) == 1:
        return int(lst[0], 2)
    if n >= len(lst[0]):
        raise ValueError("Invalid bit position.")

    most = sum(int(x[n]) for x in lst)
    logging.info(f"{most=}")
    if most >= len(lst) / 2:
        # Most common value is 1
        # Least common value is 0
        logging.info("Most common value is 1")
        next_lst = [x for x in lst if x[n] == bit]
    elif most < len(lst) / 2:
        # Most common value is 0
        # Least common value is 1
        logging.info("Most common value is 0")
        next_lst = [x for x in lst if x[n] != bit]
    return filter_(next_lst, bit, n + 1)


logging.info("Oxygen generator rating")
oxygen_rating = filter_(data, "1")
logging.info("CO2 scrubber rating")
co2_rating = filter_(data, "0")

out = oxygen_rating * co2_rating
print(f"The life support rating is {out}")
