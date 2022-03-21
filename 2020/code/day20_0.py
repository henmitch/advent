"""https://adventofcode.com/2020/day/20"""
import functools
import operator
import re

import boilerplate as bp

Tile = list[list[str]]
Edge = tuple[int, ...]
Edges = set[Edge]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> dict[int, Tile]:
    with open(path, "r") as f:
        raw = f.read().split("\n\n")
    out = {}
    for tile in raw:
        name, *tile = tile.split("\n")
        out[int(re.search(r"\d+", name).group(0))] = tileify(tile)
    return out


def tileify(l: list[str]) -> Tile:
    return [list(line) for line in l]


def get_edge_coordinates(tile: Tile) -> tuple[tuple[int, ...]]:
    top = tuple(i for i, val in enumerate(tile[0]) if val == "#")
    bottom = tuple(i for i, val in enumerate(tile[-1]) if val == "#")
    left = tuple(i for i, row in enumerate(tile) if row[0] == "#")
    right = tuple(i for i, row in enumerate(tile) if row[-1] == "#")
    return top, bottom, left, right


def get_pairwise_differences(nums: tuple[int, ...], l: int) -> Edge:
    out = list(nums)
    for i, num1 in enumerate(nums):
        for j, num2 in enumerate(nums):
            if j > i:
                out.append(abs(num1 - num2))
        out.append(l - num1)
    return tuple(sorted(out))


def get_edge_differences(tile: Tile) -> Edges:
    l = len(tile) - 1
    edges = get_edge_coordinates(tile)
    return tuple(get_pairwise_differences(edge, l) for edge in edges)


def get_all_edge_differences(tiles: dict[int, Tile]) -> dict[int, Edges]:
    out = tiles.copy()
    for tile_id, tile in tiles.items():
        out[tile_id] = get_edge_differences(tile)
    return out


def find_matches(base_tile_id: int, edgeses: dict[int, Edges]) -> list[int]:
    base_edges = edgeses[base_tile_id]
    out = []
    for tile_id, edges in edgeses.items():
        if tile_id == base_tile_id:
            continue
        if set(edges) & set(base_edges):
            out.append(tile_id)
    return out


def find_corners(tiles: dict[int, Tile]) -> list[int]:
    all_edge_differences = get_all_edge_differences(tiles)
    corners = []
    for tile_id in tiles:
        if len(find_matches(tile_id, all_edge_differences)) == 2:
            corners.append(tile_id)
    if len(corners) != 4:
        raise ValueError(f"Found {len(corners)} corners")
    return corners


def corner_product(tiles: dict[int, Tile]) -> list[int]:
    corners = find_corners(tiles)
    return functools.reduce(operator.mul, corners)


def test():
    test_data = load_data(TEST_PATH)
    assert corner_product(test_data) == 20899048083289


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(corner_product(data))
