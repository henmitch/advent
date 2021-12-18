"""https://adventofcode.com/2021/day/2"""
import re

import boilerplate as bp

path = bp.get_data_path()
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
