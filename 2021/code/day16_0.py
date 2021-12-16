"""https://adventofcode.com/2021/day/16"""
from __future__ import annotations

import os
from typing import List

import boilerplate as bp

DATA_PATH = os.path.join(bp.data_dir, "day16.txt")
TEST_PATH = os.path.join(bp.test_dir, "day16.txt")


def load_data(path):
    with open(path, "r") as f:
        raw = f.read()
    return process(raw)


def process(data: str) -> str:
    """Convert the hex to binary"""
    l = 4*len(data)
    hex = int(data, 16)
    return str(bin(hex))[2:].zfill(l)


class Packet():
    def __init__(self, packet: str):
        self.packet = packet
        self.version = self.get_version()
        self.type = self.get_type()
        self.data = packet[6:]
        self.literal = self.type == 4

    def __repr__(self):
        return (f"Packet({'literal' if self.literal else 'operator'} "
                f"v{self.version} t{self.type})")

    def get_version(self) -> int:
        return int(self.packet[:3], 2)

    def get_type(self) -> int:
        return int(self.packet[3:6], 2)

    def get_literal_data(self) -> str:
        if not self.literal:
            raise ValueError("Not a literal packet")
        out = ""
        current_idx = 0
        while True:
            out += self.data[current_idx + 1:current_idx + 5]
            if self.data[current_idx] == "0":
                break
            current_idx += 5

        return out

    def get_literal_value(self) -> int:
        return int(self.get_literal_data(), 2)

    def given_length(self) -> int | bool:
        if self.literal:
            raise ValueError("Not an operator packet")
        length_bit = self.data[0]
        if length_bit == "0":
            return int(self.data[1:16], 2)
        return False

    def get_subpackets(self) -> List[Packet]:
        if (l_subpackets := self.given_length()) is not False:
            if len(self.data) < 16 + l_subpackets:
                raise ValueError("Invalid operator packet; too short")
            out = []
            # Zeroth bit is the indicator bit
            # Bits 1-15 are the length of the subpackets
            # Bits 16-16+l_subpackets - 1 (inclusive) are the subpackets
            data = self.data[16:16 + l_subpackets]
            while True:
                # Create packets until they're no longer valid
                try:
                    p = Packet(data)
                except ValueError:
                    break
                out.append(p)
                data = p.remainder()
            return out

        out = []
        # Zeroth bit is the indicator bit
        # Bits 1-11 are the number of subpackets
        # Bits 12- are the potential subpackets
        n_subpackets = int(self.data[1:12], 2)
        data = self.data[12:]
        while len(out) < n_subpackets:
            # We shouldn't need a try/except here, since we should be able to
            # get the right number of subpackets
            p = Packet(data)
            out.append(p)
            data = p.remainder()
        return out

    def get_all_data(self) -> str:
        out = self.packet[:6]
        if self.literal:
            l = len(self.get_literal_data())
            # out += self.data[:int(l*1.25)]
            out += self.data[:int(l*1.25)]
        elif self.given_length() is not False:
            out += self.data[:16 + self.given_length()]
        else:
            out += self.data[:12]
            out += "".join(p.get_all_data() for p in self.get_subpackets())
        return out

    def remainder(self) -> str:
        return self.packet[len(self.get_all_data()):]

    def flatten(self) -> iter[Packet]:
        yield self
        if not self.literal:
            for packet in self.get_subpackets():
                yield from packet.flatten()

    def version_sum(self) -> int:
        return sum(p.version for p in self.flatten())


def parse(data: str):
    out = []
    p = Packet(data)
    while True:
        out += [packet for packet in p.flatten()]
        if r := p.remainder():
            try:
                p = Packet(r)
            except ValueError:
                break
        else:
            break
    return out


def test():
    p1 = Packet(process("D2FE28"))
    assert p1.version == 6
    assert p1.type == 4
    assert p1.literal
    assert p1.get_literal_value() == 2021
    p2 = Packet(process("38006F45291200"))
    for i, p in enumerate(p2.flatten()):
        if p.literal:
            assert p.get_literal_value() == (i)*10
    p3 = Packet(process("EE00D40C823060"))
    for i, p in enumerate(p3.flatten()):
        if p.literal:
            assert p.get_literal_value() == i

    assert (Packet(process("8A004A801A8002F478")).version_sum() == 16)
    assert (Packet(process("620080001611562C8802118E34")).version_sum() == 12)
    assert (Packet(
        process("C0015000016115A2E0802F182340")).version_sum() == 23)
    assert (Packet(
        process("A0016C880162017C3686B18A3D4780")).version_sum() == 31)

    # Remainders aren't cooperating.
    # Version 0, type 0, length 0, 1 subpacket
    # That subpacket will be a literal with value 0 and 2 extra zeros
    literal_0 = "000" "100" "10000" "00000"
    extra = "0000000000000000"
    p4 = Packet("000" "000" "1" "00000000010" + 2*literal_0 + extra)
    assert p4.remainder() == extra
    assert p4.get_subpackets()[0].get_literal_value() == 0
    assert p4.get_subpackets()[1].get_literal_value() == 0

    print("Passed tests")


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    p = Packet(data)
    print(p.version_sum())
