"""https://adventofcode.com/2021/day/24"""
from typing import Callable, Dict, Optional, Tuple

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

ALU = Dict[str, int]
Operation = Callable[[str, str | int, ALU], ALU]
Instruction = Tuple[Operation, str, Optional[str | int]]

# w will always be the last digit that we input. That's probably pretty big.


def inp(a: str, val: int, alu: ALU) -> ALU:
    # We can use shallow copies (thank god) because the ALU only contains ints.
    alu = alu.copy()
    alu[a] = val
    return alu


def add(a: str, b: str | int, alu: ALU) -> ALU:
    alu = alu.copy()
    if isinstance(b, str):
        alu[a] = alu[a] + alu[b]
    else:
        alu[a] = alu[a] + b
    return alu


def mul(a: str, b: str | int, alu: ALU) -> ALU:
    alu = alu.copy()
    if isinstance(b, str):
        alu[a] = alu[a]*alu[b]
    else:
        alu[a] = alu[a]*b
    return alu


def div(a: str, b: str | int, alu: ALU) -> ALU:
    alu = alu.copy()
    if isinstance(b, str):
        alu[a] = alu[a]//alu[b]
    else:
        alu[a] = alu[a]//b
    return alu


def mod(a: str, b: str, alu: ALU) -> ALU:
    alu = alu.copy()
    if isinstance(b, str):
        alu[a] = alu[a]%alu[b]
    else:
        alu[a] = alu[a]%b
    return alu


def eql(a: str, b: str | int, alu: ALU) -> ALU:
    alu = alu.copy()
    if isinstance(b, str):
        alu[a] = int(alu[a] == alu[b])
    else:
        alu[a] = int(alu[a] == b)
    return alu


OPS = {f.__name__: f for f in [inp, add, mul, div, mod, eql]}


def is_valid(alu: ALU) -> bool:
    return alu["z"] == 0


def load_data(path: str) -> Tuple[Instruction]:
    with open(path, "r") as f:
        lines = f.read().splitlines()
    out = []
    for line in lines:
        # So I can add comments
        if "#" in line:
            line = line[:line.index("#")]
        if line == "":
            continue

        line = line.split()
        if len(line) == 3:
            try:
                line[2] = int(line[2])
            except ValueError:
                pass
        out.append(tuple((OPS[line[0]], (*line[1:], ))))
    return tuple(out)


def run(instructions: Tuple[Instruction],
        num: int,
        n_to_run: int = None) -> ALU:
    alu = {l: 0 for l in "wxyz"}
    num = list(str(num))
    if len(num) != (n := len(chunk_up(instructions))):
        raise ValueError(f"Number must be {n} digits long")

    if n_to_run is not None:
        instructions = instructions[:n_to_run]

    for row in instructions:
        if row[0] == inp:
            alu = row[0](*row[1], int(num.pop(0)), alu)
        else:
            alu = row[0](*row[1], alu)
    return alu


def chunk_up(instructions: Tuple[Instruction]) -> Tuple[Tuple[Instruction]]:
    out = []
    to_add = [instructions[0]]
    idx = 1
    while True:
        for row in instructions[idx:]:
            if row[0] == inp:
                break
            to_add.append(row)
        else:
            out.append(tuple(to_add))
            break

        out.append(tuple(to_add))
        idx += len(to_add)
        to_add = [row]
    return tuple(out)


# 00 inp w
# 01 mul x 0  <-- Sets x to 0
# 02 add x z  <-- Sets x to z
# 03 mod x 26 <-- Sets x to z mod 26
# 04 div z a  <-- This changes
# 05 add x b  <-- This changes
# 06 eql x w  <--| If x == w, set x to 0,
# 07 eql x 0  <--| otherwise set x to 1.
# 08 mul y 0  <-- Sets y to 0
# 09 add y 25 <-- Sets y to 25
# 10 mul y x  <-- Sets y to cx
# 11 add y 1  <-- Sets y to 25x+1
# 12 mul z y  <-- Sets z to z*(25x + 1)
# 13 mul y 0  <-- Sets y to 0
# 14 add y w  <-- Sets y to w
# 15 add y c  <-- This changes
# 16 mul y x  <-- Sets y to x(w + d)
# 17 add z y  <-- Sets z to z+x(w + d)


def extract(chunk: Tuple[Instruction]) -> Tuple[int, int, int, int]:
    return tuple(chunk[i][-1][-1] for i in [4, 5, 15])


def brute(instructions: Tuple[Operation, str, int]) -> int:
    n = len(chunk_up(instructions))
    top = int(n*"9")
    bottom = int(n*"1")
    for i in range(top, bottom, -1):
        if "0" in str(i):
            continue
        if is_valid(run(instructions, i)):
            return i


def test():
    data = load_data(DATA_PATH)
    assert run(instructions=data, num=91699394894995)["z"] == 0
    assert run(instructions=data, num=51147191161261)["z"] == 0


if __name__ == "__main__":
    test()
