"""https://adventofcode.com/2020/day/12"""
from typing import Tuple
import boilerplate as bp
from day12_0 import Boat, load_data

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

class FancyBoat(Boat):
    def __init__(self) -> None:
        super().__init__()
        self.waypoint = 10 + 1j

    def apply(self, let: str, num: int) -> None:
        match let:
            case "N":
                self.waypoint += (0 + 1j)*num
            case "S":
                self.waypoint += (0 - 1j)*num
            case "E":
                self.waypoint += (1 + 0j)*num
            case "W":
                self.waypoint += (-1 + 0j)*num
            case "L":
                self.waypoint *= (0 + 1j)**(num/90)
            case "R":
                self.waypoint *= (0 - 1j)**(num/90)
            case "F":
                self.pos += self.waypoint*num


def run(instructions: Tuple[Tuple[str, int], ...]) -> int:
    boat = FancyBoat()
    for let, num in instructions:
        boat.apply(let, num)
    return boat.distance()


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 286


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(run(data))
