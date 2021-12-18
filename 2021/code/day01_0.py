"""https://adventofcode.com/2021/day/1"""
import boilerplate as bp

path = bp.get_data_path()

with open(path, "r") as f:
    data = f.readlines()

out = sum([
    int(second) > int(first)
    for first, second in zip(data, data[1:] + data[:1])
])
print(out)
