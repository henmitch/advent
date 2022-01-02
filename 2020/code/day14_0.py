"""https://adventofcode.com/2020/day/14"""
import re
from typing import Callable, Dict, Tuple

import boilerplate as bp

MaskFunction = Callable[[str], int]
Pair = Tuple[int, int]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> Tuple[Tuple[MaskFunction | Pair, ...], ...]:
    mask_line = re.compile(r"^mask = (?P<mask>[X01]+)$")
    mem_line = re.compile(r"^mem\[(?P<addr>\d+)\] = (?P<val>\d+)")
    with open(path, "r") as f:
        raw = f.read().splitlines()
    out = []
    to_add = []
    for row in raw:
        if match := re.match(mask_line, row):
            out.append(tuple(to_add))
            to_add = [make_mask_function(match.group("mask"))]
        elif match := re.match(mem_line, row):
            to_add.append((int(match.group("addr")), int(match.group("val"))))
    out.append(tuple(to_add))
    return tuple(out[1:])


def make_mask_function(mask: str) -> MaskFunction:
    def mask_function(num: int) -> int:
        out = ""
        for num_char, mask_char in zip(bits(num), mask, strict=True):
            if mask_char == "X":
                out += num_char
            else:
                out += mask_char
        return int(out, 2)

    return mask_function


def bits(num: int, l: int = 36) -> str:
    return bin(num)[2:].rjust(l, "0")


def apply_mask(data: Tuple) -> Dict[int, int]:
    out = {}
    mask_function = data[0]
    for addr, val in data[1:]:
        out[addr] = mask_function(val)
    return out


def apply_all_masks(data: Tuple[Tuple]) -> Dict[int, int]:
    out = {}
    for group in data:
        applied = apply_mask(group)
        for addr, val in applied.items():
            out[addr] = val
    return out


def run(data: Tuple[Tuple]) -> int:
    return sum(apply_all_masks(data).values())


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 165


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(run(data))
