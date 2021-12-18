"""https://adventofcode.com/2021/day/1"""
import boilerplate as bp

path = bp.get_data_path()
with open(path, "r") as f:
    data = [int(x) for x in f.readlines()]

out = sum([
    sum([first, second, third]) < sum([second, third, fourth])
    for first, second, third, fourth in zip(
        *[data[i:] + data[:i] for i in range(4)])
])
print(out)
