"""https://adventofcode.com/2020/day/8"""
from typing import Tuple

import day08_0 as old


def uncorrupt(instructions: Tuple[Tuple[callable, int]]) -> int:
    p = old.Program()
    while True:
        try:
            instruction, val = instructions[p.idx]
        except IndexError:
            return p.accumulator
        try:
            if instruction == "nop":
                p.nop(val)
            elif instruction == "acc":
                p.acc(val)
            elif instruction == "jmp":
                p.jmp(val)
        except ValueError:
            return -1


def run(instructions: Tuple[Tuple[callable, int]]) -> int:
    instructions = list(instructions)
    for i in range(len(instructions) - 1, 0, -1):
        command, val = instructions[i]
        if command not in ["jmp", "nop"]:
            continue
        modified = instructions.copy()

        if command == "jmp":
            modified[i] = ("nop", val)
        else:
            modified[i] = ("jmp", val)

        if (out := uncorrupt(modified)) < 0:
            continue
        else:
            return out
    else:
        raise ValueError("Nothing found")


def test():
    data = old.load_data(old.TEST_PATH)
    assert run(data) == 8


if __name__ == "__main__":
    test()
    data = old.load_data(old.DATA_PATH)
    print(run(data))
