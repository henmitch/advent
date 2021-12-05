import os

data_dir = os.path.join(os.path.dirname(__file__), "data")

path = os.path.join(data_dir, "day01_0.txt")

with open(path, "r") as f:
    data = f.readlines()

out = sum([
    int(second) > int(first)
    for first, second in zip(data, data[1:] + data[:1])
])
