"""https://adventofcode.com/2020/day/14"""
import re
from typing import Dict, Tuple

from day14_0 import (DATA_PATH, MaskFunction, Pair, bits)


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
            to_add = [make_addr_mask_function(match.group("mask"))]

        elif match := re.match(mem_line, row):
            to_add.append((int(match.group("addr")), int(match.group("val"))))
    out.append(tuple(to_add))
    return tuple(out[1:])


def make_addr_mask_function(mask: str) -> MaskFunction:
    def addr_mask_function(num: int) -> Tuple[int]:
        outs = [""]
        for num_char, mask_char in zip(bits(num), mask, strict=True):
            if mask_char == "0":
                new_outs = []
                for out in outs:
                    new_outs.append(out + num_char)
                outs = new_outs
            elif mask_char == "1":
                new_outs = []
                for out in outs:
                    new_outs.append(out + "1")
                outs = new_outs
            else:
                new_outs = []
                for out in outs:
                    new_outs.append(out + "0")
                    new_outs.append(out + "1")
                outs = new_outs

        return tuple(map(lambda x: int(x, 2), outs))

    return addr_mask_function


def apply_mask(data: Tuple) -> Dict[int, int]:
    out = {}
    addr_mask_function = data[0]
    for addr, val in data[1:]:
        for masked_addr in addr_mask_function(addr):
            out[masked_addr] = val
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
    data = ((make_addr_mask_function("000000000000000000000000000000X1001X"),
             (42, 100)),
            (make_addr_mask_function("00000000000000000000000000000000X0XX"),
             (26, 1)))
    assert run(data) == 208
    print("Passed tests")


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(run(data))
