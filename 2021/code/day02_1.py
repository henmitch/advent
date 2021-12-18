"""https://adventofcode.com/2021/day/2"""
import re

import boilerplate as bp

path = bp.get_data_path()
with open(path, "r") as f:
    data = f.readlines()

forward = 0
down = 0
aim = 0

for line in data:
    if line.startswith("forward"):
        x = int(re.findall(r"\d+", line)[0])
        forward += x
        down += x*aim
    elif line.startswith("down"):
        x = int(re.findall(r"\d+", line)[0])
        aim += x
    elif line.startswith("up"):
        x = int(re.findall(r"\d+", line)[0])
        aim -= x

out = forward*down

print(out)
