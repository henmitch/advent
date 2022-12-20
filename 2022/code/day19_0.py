"""https://adventofcode.com/2022/day/19"""
import re
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


def bots_available(rocks: Rocks, blueprint: Blueprint) -> Bots:
    return tuple(
        all(rock >= need for rock, need in zip(rocks, needs))
        for needs in blueprint[1:])


def most_rocks(blueprint: Blueprint) -> Rocks:
    return tuple(map(max, zip(*blueprint[1:])))


def make_bot(idx: int, rocks: Rocks, bots: Bots,
             blueprint: Blueprint) -> tuple[Rocks, Bots]:
    to_make = blueprint[idx + 1]
    new_bots = tuple(bot + int(i == idx) for i, bot in enumerate(bots))
    new_rocks = tuple(rock + bot - cost
                      for rock, bot, cost in zip(rocks, bots, to_make))
    return new_rocks, new_bots


def mine_rocks(rocks: Rocks, bots: Bots) -> Rocks:
    return tuple(rock + bot for rock, bot in zip(rocks, bots))


def ideal_world(time: int, rocks: Rocks, bots: Bots,
                blueprint: Blueprint) -> int:
    """Whether, in an ideal world where we can build anything at a given time,
    we could get more geodes"""
    for _ in range(time):
        for i, bot in enumerate(bots_available(rocks, blueprint)):
            rocks = mine_rocks(rocks, bots)
            if not bot:
                continue
            to_make = blueprint[i + 1]
            new_bots = tuple(bot + int(j == i) for j, bot in enumerate(bots))
            new_rocks = tuple(rock - cost
                              for rock, cost in zip(rocks, to_make))
            rocks = tuple(map(min, zip(rocks, new_rocks)))
            bots = tuple(map(max, zip(bots, new_bots)))
    return rocks[-1]


def find_max_geodes(blueprint: Blueprint, duration: int = 24) -> int:
    mosts = most_rocks(blueprint)

    start_time = 0
    start_rocks = (0, 0, 0, 0)
    start_bots = (1, 0, 0, 0)

    to_check = {(start_time, start_rocks, start_bots)}
    out = 0
    pruner = (duration + 1, 0)

    steps = 0
    while to_check:
        time, rocks, bots = to_check.pop()
        # If we have a geode, then we can ignore any possibilities with fewer
        # geodes by now
        if rocks[-1]:
            if time > pruner[0] and rocks[-1] < pruner[1]:
                continue
            else:
                pruner = (time, rocks[-1])
        elif time >= pruner[0]:
            continue

        ideal = ideal_world(duration - time, rocks, bots, blueprint)
        if ideal < max(1, pruner[1]):
            continue

        # Once we reach `duration` minutes, we stop
        if time == duration or (time == duration - 1 and not bots[-1]):
            out = max(out, rocks[-1])
            continue

        next_time = time + 1

        avail = bots_available(rocks, blueprint)
        # If we can get a geode bot, get it and ignore other possibilities
        if avail[-1]:
            to_check.add((next_time, *make_bot(3, rocks, bots, blueprint)))
            continue

        # Otherwise, see about building each of the other bots
        for i, bot in enumerate(avail[:-1]):
            if not bot:
                continue
            next_rocks, next_bots = make_bot(i, rocks, bots, blueprint)
            if any(bot > most
                   for bot, most in zip(next_bots[:-1], mosts[:-1])):
                continue
            to_check.add((next_time, next_rocks, next_bots))

        next_rocks = mine_rocks(rocks, bots)
        to_check.add((next_time, next_rocks, bots))
        steps += 1
        if not steps%10000:
            print(steps)

    print(blueprint[0], out)
    return out


def quality(blueprint: Blueprint) -> int:
    return find_max_geodes(blueprint)*blueprint[0]


def run(data: list[Blueprint]) -> int:
    return sum(quality(blueprint) for blueprint in data)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 33
    print("Passed")

    data = load_data(DATA_PATH)
    print(find_max_geodes(data[1]))


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    # main()
