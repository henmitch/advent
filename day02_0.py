"""https://adventofcode.com/2021/day/2"""
import os
import re

data_dir = os.path.join(os.path.dirname(__file__), "data")
path = os.path.join(data_dir, "day02_0.txt")
with open(path, "r") as f:
    data = f.readlines()

forward = 0
down = 0

for line in data:
    if line.startswith("forward"):
        forward += int(re.findall(r"\d+", line)[0])
    elif line.startswith("down"):
        down += int(re.findall(r"\d+", line)[0])
    elif line.startswith("up"):
        down -= int(re.findall(r"\d+", line)[0])

out = forward * down

print(out)
