"""https://adventofcode.com/2024/day/13"""
import re

import boilerplate as bp

Claw = tuple[int, int, int, int, int, int]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[Claw]:
    with open(path, "r") as f:
        raw = f.read().split("\n\n")
    return [parse(block) for block in raw]


def parse(block: str) -> Claw:
    # Using regex because I'm too lazy to write a parser
    ints = re.findall(r"\d+", block)
    return tuple(map(int, ints))


def solve(claw: Claw) -> tuple[int, int]:
    # Sometimes, naive solutions work.
    xa, ya, xb, yb, xp, yp = claw
    prize = xp + yp*1j
    for a in range(101):
        if a*xa > xp or a*ya > yp:
            break
        if a*xa + 100*xb < xp or a*ya + 100*yb < yp:
            continue
        for b in range(101):
            solution = a*(xa + ya*1j) + b*(xb + yb*1j)
            if solution.real > xp or solution.imag > yp:
                break
            if solution == prize:
                return a, b
    return -1, -1


def check(claw: Claw, a: int, b: int) -> bool:
    xa, ya, xb, yb, xp, yp = claw
    return a*(xa + ya) == xp and b*(xb + yb) == yp


def run(data: list[Claw]) -> int:
    out = 0
    for claw in data:
        a, b = solve(claw)
        if a != -1:
            out += 3*a + b
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 480


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
