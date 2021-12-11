"""https://adventofcode.com/2021/day/1"""
import os

data_dir = os.path.join(os.path.dirname(__file__), "data")
path = os.path.join(data_dir, "day01_0.txt")
with open(path, "r") as f:
    data = [int(x) for x in f.readlines()]

out = sum([
    sum([first, second, third]) < sum([second, third, fourth])
    for first, second, third, fourth in zip(
        *[data[i:] + data[:i] for i in range(4)])
])
