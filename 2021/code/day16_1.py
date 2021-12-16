"""https://adventofcode.com/2021/day/16"""
from __future__ import annotations

import operator
from functools import reduce
from typing import List

import day16_0 as old


class FancyPacket(old.Packet):
    def __init__(self, packet: str):
        super().__init__(packet)

    def get_value(self) -> int:
        if self.literal:
            return self.get_literal_value()
        else:
            return self.get_operator_value()

    def get_subpackets(self) -> List[FancyPacket]:
        return [FancyPacket(p.packet) for p in super().get_subpackets()]

    def get_operator_value(self) -> int:
        vals = [p.get_value() for p in self.get_subpackets()]
        if self.type == 0:
            return sum(vals)
        elif self.type == 1:
            return reduce(operator.mul, vals)
        elif self.type == 2:
            return min(vals)
        elif self.type == 3:
            return max(vals)
        elif self.type == 5:
            return int(vals[0] > vals[1])
        elif self.type == 6:
            return int(vals[0] < vals[1])
        elif self.type == 7:
            return int(vals[0] == vals[1])


def test():
    assert FancyPacket(old.process("C200B40A82")).get_value() == 3
    assert FancyPacket(old.process("04005AC33890")).get_value() == 54
    assert FancyPacket(old.process("880086C3E88112")).get_value() == 7
    assert FancyPacket(old.process("CE00C43D881120")).get_value() == 9
    assert FancyPacket(old.process("D8005AC2A8F0")).get_value() == 1
    assert FancyPacket(old.process("F600BC2D8F")).get_value() == 0
    assert FancyPacket(old.process("9C005AC2F8F0")).get_value() == 0
    assert FancyPacket(
        old.process("9C0141080250320F1802104A08")).get_value() == 1


if __name__ == "__main__":
    test()
    data = old.load_data(old.DATA_PATH)
    print(FancyPacket(data).get_value())
