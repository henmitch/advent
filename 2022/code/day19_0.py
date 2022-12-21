"""https://adventofcode.com/2022/day/19"""
import re
from math import ceil

import boilerplate as bp

Rocks = tuple[int, int, int, int]
Bots = tuple[int, int, int, int]
Blueprint = tuple[int, Rocks, Rocks, Rocks, Rocks]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def parse(line: str) -> Blueprint:
    numbers = list(map(int, re.findall(r"(\d+)", line)))
    num, ore, clay, obs_o, obs_c, geode_o, geode_obs = numbers
    return (
        num,
        (ore, 0, 0, 0),
        (clay, 0, 0, 0),
        (obs_o, obs_c, 0, 0),
        (geode_o, 0, geode_obs, 0),
    )


def load_data(path: str) -> list[Blueprint]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return [parse(line) for line in raw]


def next_bots(rocks: Rocks,
              bots: Bots,
              blueprint: Blueprint,
              time: int,
              duration: int = 24) -> set[tuple[int, Rocks, Bots]]:
    """Return all next possible bots"""
    out = set()
    # Go through each possible bot
    for i in range(4):
        # The blueprint for the current bot
        botprint = blueprint[i + 1]
        # See whether we have the necessary equipment to build it
        if any(need and not have for need, have in zip(botprint, bots)):
            # Bail if we don't
            continue

        # Find the time it would take to build it
        time_taken = max(1 + ceil((need - have)/bot)
                         for need, have, bot in zip(botprint, rocks, bots)
                         if need > 0)
        # If we could've built it before,
        if time_taken <= 0:
            # don't.
            continue

        new_time = time + time_taken
        # If we're past `duration` minutes,
        if new_time >= duration:
            # show us the world where we don't build any bots
            out |= {(duration,
                     tuple(have + (duration - time)*bot
                           for have, bot in zip(rocks[:-1], bots[:-1])) +
                     (rocks[-1], ), bots)}
            continue

        # Otherwise, build it.
        # If we're building a geode bot, count all its contributions to the end
        if i == 3:
            new_bots = bots[:i] + (bots[i] + 1, )
            new_rocks = tuple(rock + time_taken*bot - need
                              for rock, bot, need in zip(
                                  rocks[:-1], bots[:-1], botprint[:-1]))
            new_rocks += (rocks[-1] + duration - new_time, )
        else:
            new_bots = bots[:i] + (bots[i] + 1, ) + bots[i + 1:]
            new_rocks = tuple(
                have + time_taken*bot - use for have, bot, use in zip(
                    rocks[:-1], bots[:-1], botprint[:-1])) + (rocks[-1], )

        out |= {(new_time, new_rocks, new_bots)}
    return out


def max_geodes(blueprint: Blueprint, duration: int = 24) -> int:
    start_time = 0
    start_rocks = (0, 0, 0, 0)
    start_bots = (1, 0, 0, 0)

    to_check = {(start_time, start_rocks, start_bots)}
    seen = set()

    time_of_first_geode = duration + 1
    out = 0

    while to_check:
        current = time, rocks, bots = max(to_check, key=lambda x: x[1][-1])
        to_check.remove(current)
        seen.add(current)
        # If we've had a geode at time t and we have no geodes at a time later
        # than t, we're barking up the wrong tree
        if time > time_of_first_geode and not rocks[-1]:
            continue
        # If we couldn't get enough geodes by building one bot per minute for
        # the remaining time, bail
        if rocks[-1] + sum(range(time, duration)) <= out:
            continue
        # If this is the best we've done (earliest to get geodes), then we
        # update our best
        if rocks[-1]:
            time_of_first_geode = min(time, time_of_first_geode)
        # The maximum number of geodes
        out = max(out, rocks[-1])
        to_check |= next_bots(rocks, bots, blueprint, time, duration) - seen

    print(blueprint[0], out)
    return out


def quality(blueprint: Blueprint, duration: int = 24) -> int:
    return blueprint[0]*max_geodes(blueprint, duration)


def run(data: list[Blueprint]) -> int:
    return sum(quality(blueprint) for blueprint in data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 33


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
