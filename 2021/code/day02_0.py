"""https://adventofcode.com/2021/day/2"""
import os
import re

import boilerplate as bp

path = os.path.join(bp.data_dir, "day02.txt")
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

out = forward*down

print(out)
