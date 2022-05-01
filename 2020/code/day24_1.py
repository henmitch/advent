"""https://adventofcode.com/2020/day/24"""
import functools
from numbers import Complex

import day24_0 as old


def step(tiles: set[Complex]) -> set[Complex]:
    out = set()
    to_checks = set()
    for tile in tiles:
        to_checks |= get_neighbors(tile)

    for to_check in to_checks:
        neighbors = get_neighbors(to_check)
        on_neighbors = neighbors & tiles
        if to_check in tiles:
            if len(on_neighbors) in {1, 2}:
                out.add(to_check)
        elif len(on_neighbors) == 2:
            out.add(to_check)
    return out


@functools.cache
def get_neighbors(base: Complex) -> set[Complex]:
    return {base + d for d in old.DIRECTIONS.values()}


def run(data: list[list[str]]) -> int:
    tiles = old.run(data)
    for _ in range(100):
        tiles = step(tiles)
    return tiles


def test():
    data = old.load_data(old.TEST_PATH)
    assert len(run(data)) == 2208


def main():
    data = old.load_data(old.DATA_PATH)
    print(len(run(data)))


if __name__ == "__main__":
    test()
    main()
