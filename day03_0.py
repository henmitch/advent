"""https://adventofcode.com/2021/day/3"""
import os

data_dir = os.path.join(os.path.dirname(__file__), "data")
path = os.path.join(data_dir, "day03_0.txt")
with open(path, "r") as f:
    data = f.read().splitlines()

gamma_str = ""

for i in range(len(data[0])):
    count = sum(int(x[i]) for x in data)
    if count > len(data)/2:
        gamma_str += "1"
    else:
        gamma_str += "0"

gamma = int(gamma_str, 2)
epsilon = gamma^int("1"*(len(data[0])), 2)

out = gamma*epsilon
print(f"The power consumption is {out}")
