"""https://adventofcode.com/2024/day/2"""
from day02_0 import DATA_PATH, TEST_PATH, load_data, is_safe


def sign(x: int) -> int:
    return (x > 0) - (x < 0)


def is_safeable(line: list[int]) -> bool:
    if is_safe(line):
        return True
    signs = [sign(b - a) for a, b in zip(line, line[1:])]
    if abs(sum(signs)) < len(signs) - 2 or signs.count(0) > 1:
        return False
    direction = sign(sum(signs))
    for i, (a, b) in enumerate(zip(line, line[1:])):
        if b - a not in (direction, 2*direction, 3*direction):
            # This is real ugly. I'm sorry.
            if i < len(line) - 2 and (
                    not is_safe(line[:i] + line[i + 1:])) and (
                        not is_safe(line[:i + 1] + line[i + 2:])):
                return False
    return True


def run(data: list[list[int]]) -> int:
    return sum(is_safeable(line) for line in data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 4


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
