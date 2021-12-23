"""https://adventofcode.com/2021/day/22"""
import boilerplate as bp
import re
from typing import List, Set, Tuple

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


# Let's do the naive approach first.
def load_data(path: str) -> List[Tuple]:
    regex = re.compile(r"^(?P<power>on|off) "
                       r"x=(?P<x_min>-?\d+)..(?P<x_max>-?\d+),"
                       r"y=(?P<y_min>-?\d+)..(?P<y_max>-?\d+),"
                       r"z=(?P<z_min>-?\d+)..(?P<z_max>-?\d+)$")
    with open(path, "r") as f:
        lines = f.read().splitlines()
    matches = [regex.match(line) for line in lines]
    return [(match.group("power"),
             order(match.group("x_min"), match.group("x_max")),
             order(match.group("y_min"), match.group("y_max")),
             order(match.group("z_min"), match.group("z_max")))
            for match in matches]


def order(s1: str, s2: str) -> Tuple[int, int]:
    return tuple(sorted([int(s1), int(s2)]))


def update_lights(on: Set[Tuple], off: set[Tuple],
                  cuboid: List[Tuple]) -> Tuple[Set]:
    power, (x_min, x_max), (y_min, y_max), (z_min, z_max) = cuboid
    if any(l > 50 or l < -50
           for l in (x_min, x_max, y_min, y_max, z_min, z_max)):
        return on, off
    to_ = on if power == "on" else off
    from_ = on if power == "off" else off
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            for z in range(z_min, z_max + 1):
                to_.add((x, y, z))
    from_ -= to_
    return on, off


def reboot(lights: List[Tuple]) -> Tuple[Set]:
    on = set()
    off = set()
    for light in lights:
        on, off = update_lights(on, off, light)
    return on, off


def test():
    data = load_data(TEST_PATH)
    on, _ = reboot(data)
    assert len(on) == 474140


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    on, _ = reboot(data)
    print(len(on))
