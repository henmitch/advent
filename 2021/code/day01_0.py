"""https://adventofcode.com/2021/day/1"""
import os

import boilerplate as bp

path = os.path.join(bp.data_dir, "day01.txt")

with open(path, "r") as f:
    data = f.readlines()

out = sum([
    int(second) > int(first)
    for first, second in zip(data, data[1:] + data[:1])
])
print(out)
