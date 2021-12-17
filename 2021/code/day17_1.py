"""https://adventofcode.com/2021/day/17"""
from day17_0 import *  # Because I'm lazy


def max_viable_x_velocity(target: Area) -> int:
    max_x = max(x for x, _ in target)
    # This is pretty much the same as the min_viable_x_velocity from the
    # previous part
    return max_x


def all_good_velocities(target: Area) -> List[Velocity]:
    velocities = []
    # We can probably do better than this
    for v_x in range(min_viable_x_velocity(target),
                     max_viable_x_velocity(target) + 1):
        # We use the negative maximum because the previous minimum was assuming
        # we were using the minimum x velocity (and shooting up).
        for v_y in range(-max_viable_y_velocity(target),
                         max_viable_y_velocity(target) + 1):
            traj = make_trajectory((v_x, v_y), target)
            if good(traj, target):
                velocities.append((v_x, v_y))
    return velocities


def count_good_trajectories(target: Area) -> int:
    return len(all_good_velocities(target))


def test():
    area = load_data(TEST_PATH)
    assert count_good_trajectories(area) == 112


if __name__ == "__main__":
    test()
    area = load_data(DATA_PATH)
    print(count_good_trajectories(area))
