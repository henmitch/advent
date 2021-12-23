"""https://adventofcode.com/2021/day/22"""
from __future__ import annotations
import functools
import re
from typing import List, Set, Tuple
from day22_0 import order, TEST_PATH, DATA_PATH


def load_data(path: str) -> List[Tuple]:
    regex = re.compile(r"^(?P<power>on|off) "
                       r"x=(?P<x_min>-?\d+)..(?P<x_max>-?\d+),"
                       r"y=(?P<y_min>-?\d+)..(?P<y_max>-?\d+),"
                       r"z=(?P<z_min>-?\d+)..(?P<z_max>-?\d+)$")
    with open(path, "r") as f:
        lines = f.read().splitlines()
    matches = [regex.match(line) for line in lines]
    return [(1 if match.group("power") == "on" else -1,
             *order(match.group("x_min"), match.group("x_max")),
             *order(match.group("y_min"), match.group("y_max")),
             *order(match.group("z_min"), match.group("z_max")))
            for match in matches]


# Keeping track of intersections (and not multi-counting them) is difficult.
# When an ON cuboid intersects another cuboid, the latter will *always* scoop
# the intersection out of the former.


class Cuboid():
    def __init__(self, power: str, x_min: int, x_max: int, y_min: int,
                 y_max: int, z_min: int, z_max: int):
        self.power = power
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max
        self.width = x_max - x_min + 1
        self.height = y_max - y_min + 1
        self.depth = z_max - z_min + 1
        self.volume = self.width*self.height*self.depth
        self.gaps: List[Cuboid] = []

    def __repr__(self) -> str:
        return f"Cuboid({self.get_volume()}, {self.power})"

    def __sub__(self, other: Cuboid) -> Cuboid:
        if not self.intersects(other):
            return self
        out = Cuboid(self.power, self.x_min, self.x_max, self.y_min,
                     self.y_max, self.z_min, self.z_max)
        out.gaps.append(self.intersection(other))
        return out

    def intersects(self, other: Cuboid) -> bool:
        """Whether this cuboid intersects the other."""
        if self.x_max < other.x_min or self.x_min > other.x_max:
            return False
        if self.y_max < other.y_min or self.y_min > other.y_max:
            return False
        if self.z_max < other.z_min or self.z_min > other.z_max:
            return False
        return True

    def get_volume(self) -> int:
        """The volume of this cuboid."""
        return self.power*self.volume

    def intersection(self, other: Cuboid) -> Cuboid:
        if not self.intersects(other):
            raise ValueError("No intersection. Check your cuboids, dummy.")
        power = 1
        return Cuboid(power, max(self.x_min, other.x_min),
                      min(self.x_max,
                          other.x_max), max(self.y_min, other.y_min),
                      min(self.y_max,
                          other.y_max), max(self.z_min, other.z_min),
                      min(self.z_max, other.z_max))


def apply_to_positive(c: Cuboid, lights: List[Tuple], step: int) -> int:
    # The amount of light to remove due to overlaps/double-counting
    removes = set()
    # The amount of light to add back
    adds = set()
    for light in lights[:step]:
        l = Cuboid(*light)
        # If the comparator (l) is ON, then we remove the overlap (because
        # we would double-count it otherwise).
        if l.power > 0:
            if c.intersects(l):
                i = c.intersection(l)
                # If l overlaps with something we've added back (i.e., that was
                # made available again by an OFF cuboid), we need to re-remove
                # it. (Or at least the part that overlaps with
                # c.intersection(l))

                # These are temporary holders for the overlaps we're removing
                # and adding back.
                removes_ = set()
                adds_ = set()
                for add in adds:
                    if i.intersects(add):
                        removes_ |= {i.intersection(add)}

                for remove in removes:
                    if i.intersects(remove):
                        adds_ |= {i.intersection(remove)}
                removes |= {i} | removes_
                adds |= adds_

        # If l powers stuff down, then we add back its overlap with [what was
        # removed].
        else:
            if c.intersects(l):
                i = c.intersection(l)
                removes_ = set()
                adds_ = set()
                for add in adds:
                    if i.intersects(add):
                        removes_ |= {i.intersection(add)}

                for remove in removes:
                    if i.intersects(remove):
                        adds_ |= {i.intersection(remove)}
                removes |= removes_
                adds |= adds_
                # for remove in removes:
                #     if i.intersects(remove):
                #         adds |= {i.intersection(remove)}

    # Now, we calculate the volume of the cuboid, and subtract the removes
    # and add the adds.
    v = c.volume
    for remove in removes:
        v -= c.intersection(remove).volume
    for add in adds:
        v += c.intersection(add).volume

    if v < 0:
        raise ValueError(f"Negative delta: {v}")

    return v


def apply_to_negative(c: Cuboid, lights: List[Tuple], step: int) -> int:
    # The amount of dark to remove due to overlaps/double-counting
    removes = set()
    # The amount light available to darken
    adds = set()
    for light in lights[:step]:
        l = Cuboid(*light)
        # If the comparator (l) is ON, then we add the overlap to adds (since
        # we'll be able to darken it)
        if l.power > 0:
            if c.intersects(l):
                i = c.intersection(l)
                # If l overlaps with something we've removed (i.e., that was
                # made available again by an ON cuboid), we need to re-remove
                # it. (Or at least the part that overlaps with
                # c.intersection(l))
                adds_ = set()
                removes_ = set()

                # This is to handle double-counting.
                for add in adds:
                    if i.intersects(add):
                        removes_ |= {i.intersection(add)}
                # This is to add back stuff we would have missed.
                for remove in removes:
                    if i.intersects(remove):
                        adds_ |= {i.intersection(remove)}
                adds |= {i} | adds_
                removes |= removes_

        # If l powers stuff down, then it makes things less available. So, we
        # remove the overlap between [l] and [what has been added].
        else:
            if c.intersects(l):
                i = c.intersection(l)
                adds_ = set()
                removes_ = set()
                for add in adds:
                    if i.intersects(add):
                        removes_ |= {i.intersection(add)}
                # This is to add back stuff we would have missed.
                for remove in removes:
                    if i.intersects(remove):
                        adds_ |= {i.intersection(remove)}
                adds |= adds_
                removes |= removes_

    v = 0
    for remove in removes:
        v += c.intersection(remove).volume
    for add in adds:
        v -= c.intersection(add).volume

    if v > 0:
        raise ValueError(f"Positive delta: {v}")

    return v


def apply(lights: List[Tuple], step: int) -> int:
    """The change in state from state i-1 to i"""
    c = Cuboid(*lights[step])  # The cuboid whose delta we want to know
    # If the cuboid is ON, we leave it ON no matter what, but subtract the
    # overlaps from the total volume.
    # EXCEPT, we don't subtract stuff that's powered down.
    if c.power > 0:
        return apply_to_positive(c, lights, step)
    return apply_to_negative(c, lights, step)


def apply_all(lights: List[Tuple]) -> int:
    out = []
    for i in range(len(lights)):
        out.append(apply(lights, i))
    return out


def count_lights(lights: Set[Cuboid]) -> int:
    """Count the number of lights that are on."""
    return sum(light.get_volume() for light in lights)


def count_intersects(lights: List[Cuboid]) -> int:
    out = []
    for i, light in enumerate(lights):
        row = [0]*(i + 1)
        for ii, other in enumerate(lights[i + 1:]):
            ii += i + 1
            if light.intersects(other):
                inter = 1
            else:
                inter = 0
            row.append(inter)
        out.append(row)
    return out


def test():
    tester = [(1, 10, 12, 10, 12, 10, 12), (1, 11, 13, 11, 13, 11, 13),
              (-1, 9, 11, 9, 11, 9, 11), (1, 10, 10, 10, 10, 10, 10)]
    assert sum(apply_all(tester)) == 39
    data = load_data(TEST_PATH)
    out = apply_all(data)
    assert sum(out) == 2758514936282235


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(sum(apply_all(data)))
