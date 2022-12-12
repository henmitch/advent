"""https://adventofcode.com/2022/day/05"""
from day05_0 import DATA_PATH, TEST_PATH, Instruction, Stack, load_data


def execute(stacks: list[Stack], instruction: Instruction) -> None:
    n, start, end = instruction
    stacks[end - 1] += stacks[start - 1][-n:]
    del stacks[start - 1][-n:]


def run(stacks: list[Stack], instructions: list[Instruction]) -> str:
    for instruction in instructions:
        execute(stacks, instruction)
    return "".join(stack[-1] for stack in stacks)


def test():
    data = load_data(TEST_PATH)
    assert run(*data) == "MCD"


def main():
    data = load_data(DATA_PATH)
    print(run(*data))


if __name__ == "__main__":
    test()
    main()
