"""https://adventofcode.com/2022/day/5"""
import re

import boilerplate as bp

Stack = list[str]
Instruction = tuple[int, int, int]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[list[Stack], list[Instruction]]:
    with open(path, "r") as f:
        raw = f.read().split("\n\n")
    # Making stacks
    stacks = make_stacks(raw[0])
    # Making instructions
    instructions = parse_instructions(raw[1])
    return stacks, instructions


def make_stacks(raw: str) -> list[Stack]:
    # Note: not generalized to double-digit stacks or multi-letter box names
    raw = raw.splitlines()
    max_len = len(raw[-1]) + 1
    n_stacks = int(raw[-1].strip()[-1])
    out = [[] for _ in range(n_stacks)]
    for line in raw[-2::-1]:
        line = line.ljust(max_len, " ")
        for stack_num in range(n_stacks):
            to_add = line[stack_num*4 + 1]
            if to_add == " ":
                pass
            else:
                out[stack_num].append(to_add)
    return out


def parse_instructions(raw: str) -> list[Instruction]:
    template = re.compile(r"move (\d+) from (\d+) to (\d+)")
    out = []
    for line in raw.splitlines():
        out.append(tuple(map(int, re.match(template, line).groups())))
    return out


def execute(stacks: list[Stack], instruction: Instruction) -> None:
    n, start, end = instruction
    for _ in range(n):
        stacks[end - 1].append(stacks[start - 1].pop())


def run(stacks: list[Stack], instructions: list[Instruction]) -> str:
    for instruction in instructions:
        execute(stacks, instruction)
    return "".join(stack[-1] for stack in stacks)


def test():
    data = load_data(TEST_PATH)
    assert run(*data) == "CMZ"


def main():
    data = load_data(DATA_PATH)
    print(run(*data))


if __name__ == "__main__":
    test()
    main()
