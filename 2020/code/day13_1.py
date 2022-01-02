"""https://adventofcode.com/2020/day/13"""
import functools
import operator
from typing import Tuple

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> Tuple[int | str, ...]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    periods = tuple(int(x) if x != "x" else "x" for x in raw[1].split(","))
    return periods


def get_coefficients(a: int, b: int) -> Tuple[int, int]:
    r0, r1 = a, b
    s0, s1 = 1, 0
    t0, t1 = 0, 1
    while True:
        q = r0//r1
        r0, r1 = r1, r0 - q*r1
        s0, s1 = s1, s0 - q*s1
        t0, t1 = t1, t0 - q*t1
        if r1 == 0:
            return s0, t0


def get_remainders(periods: Tuple[int | str, ...]) -> Tuple[Tuple[int, int]]:
    out = []
    for i, period in enumerate(periods):
        if not isinstance(period, int):
            continue
        out.append(((period - i)%period, period))
    return tuple(out)


# https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Case_of_two_moduli
def run(periods: Tuple[int | str, ...]) -> int:
    periods = get_remainders(periods)
    N = functools.reduce(operator.mul, (period[1] for period in periods))
    out = 0
    for a, n in periods:
        if n == "x":
            continue
        y = N//n
        z, _ = get_coefficients(y, n)
        out += a*z*y
    return out%N


def test():
    run((7, 13))
    data = load_data(TEST_PATH)
    assert run(data) == 1068781
    assert run((67, 7, 59, 61)) == 754018
    assert run((67, "x", 7, 59, 61)) == 779210
    assert run((67, 7, "x", 59, 61)) == 1261476
    assert run((1789, 37, 47, 1889)) == 1202161486


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(run(data))
