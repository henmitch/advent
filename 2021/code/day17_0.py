"""https://adventofcode.com/2021/day/17"""
import math
import os
import re
from typing import List, Set, Tuple

import boilerplate as bp

Point = Velocity = Tuple[int, int]
Area = Trajectory = List[Point]

DATA_PATH = os.path.join(bp.data_dir, "day17.txt")
TEST_PATH = os.path.join(bp.test_dir, "day17.txt")


def load_data(path) -> Area:
    with open(path, "r") as f:
        raw = f.read()
    extraction = re.compile(r"x=(?P<x1>-?\d+)\.\.(?P<x2>-?\d+), "
                            r"y=(?P<y1>-?\d+)\.\.(?P<y2>-?\d+)")
    data = re.search(extraction, raw).groupdict()
    x1, x2 = sorted((int(data["x1"]), int(data["x2"])))
    y1, y2 = sorted((int(data["y1"]), int(data["y2"])))
    return {(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)}


def sign(x: int) -> int:
    if x == 0:
        return 0
    return abs(x)/x


def step(r: Point, v: Velocity) -> Tuple[Point, Velocity]:
    x, y = r
    v_x, v_y = v
    r_out = (x + v_x, y + v_y)
    v_out = (v_x - sign(v_x), v_y - 1)
    return r_out, v_out


def good(traj: Trajectory, area: Area) -> bool:
    return bool(set(traj) & area)


def max_height(traj: Trajectory) -> int:
    return max(y for _, y in traj)


def make_trajectory(v0: Velocity, target: Area) -> Trajectory:
    # Largest x, smallest y
    lowest, furthest = min(target,
                           key=lambda x: x[1])[1], max(target,
                                                       key=lambda x: x[0])[0]
    v = v0
    r = (0, 0)
    traj = [r]
    while not good(traj, target):
        r, v = step(r, v)
        if r[0] > furthest or r[1] < lowest:
            break
        traj.append(r)
    return traj


def biggest_drop(traj: Trajectory) -> int:
    # We only care about when it's going down, i.e., when
    # traj[i][1] < traj[i+1][1]
    return abs(min(y2 - y1 for (_, y1), (_, y2) in zip(traj, traj[1:])))


def min_viable_x_velocity(target: Area) -> int:
    min_x = min(x for x, _ in target)
    # Total distance traveled x will be v0 + (v0-1) + (v0-2)... = (v0 + 1)*v0/2
    # So, the v0 to travel x will be...
    return int(math.ceil((-1 + math.sqrt(1 + 8*min_x))/2))


def min_viable_y_velocity(target: Area) -> int:
    v = (min_viable_x_velocity(target), 0)
    traj = make_trajectory(v, target)
    while not good(traj, target):
        v = (v[0], v[1] + 1)
        traj = make_trajectory(v, target)

    return v[1]


def max_viable_y_velocity(target: Area) -> int:
    # Shooting straight down will give the same result y-wise, so the maximum
    # possible y-velocity is the magnitude of the lowest point in the target
    return abs(min(y for _, y in target))


def find_max_y(target: Area) -> int:
    v_x = min_viable_x_velocity(target)
    max_ys = []
    for v_y in range(min_viable_y_velocity(target),
                     max_viable_y_velocity(target) + 1):
        traj = make_trajectory((v_x, v_y), target)
        if good(traj, target):
            max_ys.append(max_height(traj))
    return max(max_ys)


def test():
    area = load_data(TEST_PATH)
    assert find_max_y(area) == 45


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(find_max_y(data))
