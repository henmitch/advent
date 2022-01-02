"""https://adventofcode.com/2020/day/12"""
from typing import Tuple
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> Tuple[Tuple[str, int], ...]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return tuple((line[0], int(line[1:])) for line in raw)


class Boat:
    def __init__(self) -> None:
        self.pos = 0 + 0j
        self.dir = 1 + 0j

    def apply(self, let: str, num: int) -> None:
        match let:
            case "N":
                self.pos += (0 + 1j)*num
            case "S":
                self.pos += (0 - 1j)*num
            case "E":
                self.pos += (1 + 0j)*num
            case "W":
                self.pos += (-1 + 0j)*num
            case "L":
                self.dir *= (0 + 1j)**(num/90)
            case "R":
                self.dir *= (0 - 1j)**(num/90)
            case "F":
                self.pos += self.dir*num

    def distance(self) -> int:
        return int(abs(self.pos.real) + abs(self.pos.imag))


def run(instructions: Tuple[Tuple[str, int], ...]) -> int:
    boat = Boat()
    for let, num in instructions:
        boat.apply(let, num)
    return boat.distance()

def test():
    data = load_data(TEST_PATH)
    assert run(data) == 25

if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(run(data))
