"""https://adventofcode.com/2020/day/20"""
import copy
import itertools
import math
import re

from day20_0 import (DATA_PATH, TEST_PATH, Tile, find_matches,
                     get_all_edge_differences, get_edge_differences, load_data)

Grid = list[list[int]]


def pretty_print(grid: Grid) -> str:
    return "\n".join([" ".join(map(str, row)) for row in grid])


def find_all_matches(tiles: dict[int, Tile]) -> dict[int, list[int]]:
    all_edge_differences = get_all_edge_differences(tiles)
    out = {
        tile_id: find_matches(tile_id, all_edge_differences)
        for tile_id in tiles
    }
    if any(len(x) not in [2, 3, 4] for x in out.values()):
        raise ValueError("Uh-oh. This is gonna be hard.")
    return out


def find_friend(*tiles: tuple[int, ...],
                matches: dict[int, list[int]],
                seen: set[int] = None) -> int:
    if seen is None:
        seen = set()
    for tile_id, friends in matches.items():
        if tile_id in seen:
            continue
        if set(tiles) <= set(friends):
            return tile_id
    raise ValueError("No friends found")


def place_tiles(tiles: dict[int, Tile]) -> Grid:
    side_length = int(math.sqrt(len(tiles)))
    out = [[None for _ in range(side_length)] for __ in range(side_length)]

    all_matches = find_all_matches(tiles)

    # We start with a corner
    tile_id = None  # Just to prevent pylint undefined-loop-variable
    for tile_id, matches in all_matches.items():
        if len(matches) == 2:
            break
    else:
        raise ValueError("No corners found")

    # Setting the top left corner
    seen = {tile_id}
    out[0][0] = tile_id
    next_to_corner = all_matches[tile_id]
    out[0][1], out[1][0] = next_to_corner
    seen |= set(next_to_corner)
    out[1][1] = find_friend(*next_to_corner, matches=all_matches, seen=seen)
    seen.add(out[1][1])

    # Now, we alternate between the top two rows
    for x in range(2, side_length):
        out[0][x] = find_friend(out[0][x - 1], matches=all_matches, seen=seen)
        seen.add(out[0][x])
        out[1][x] = find_friend(out[0][x],
                                out[1][x - 1],
                                matches=all_matches,
                                seen=seen)
        seen.add(out[1][x])

    for y in range(2, side_length):
        out[y][0] = find_friend(out[y - 1][0], matches=all_matches, seen=seen)
        seen.add(out[y][0])
        for x in range(1, side_length):
            out[y][x] = find_friend(out[y - 1][x],
                                    out[y][x - 1],
                                    matches=all_matches,
                                    seen=seen)
            seen.add(out[y][x])

    return out


def flip_over_y(tile: Tile) -> Tile:
    return [row[::-1] for row in tile]


def flip_over_x(tile: Tile) -> Tile:
    return tile[::-1]


def rotate_clockwise(tile: Tile) -> Tile:
    return [[row[i] for row in tile] for i in range(len(tile))]


TRANSFORMATIONS = (flip_over_x, flip_over_y, rotate_clockwise,
                   rotate_clockwise, rotate_clockwise)


def properly_oriented(tile: Tile,
                      top: Tile = None,
                      bottom: Tile = None,
                      left: Tile = None,
                      right: Tile = None) -> bool:
    if top is not None and top[-1] != tile[0]:
        return False
    if bottom is not None and bottom[0] != tile[1]:
        return False
    if left is not None and [r[-1] for r in left] != [r[0] for r in tile]:
        return False
    if right is not None and [r[0] for r in right] != [r[-1] for r in tile]:
        return False
    return True


def orient_tile(tile: Tile,
                top: Tile = None,
                bottom: Tile = None,
                left: Tile = None,
                right: Tile = None) -> Grid:
    # This assumes that the top, bottom, left, and right tiles are fixed
    neighbors = top, bottom, left, right
    if properly_oriented(tile, *neighbors):
        return tile

    for transformation in set(TRANSFORMATIONS):
        if properly_oriented(transformation(tile), *neighbors):
            return transformation(tile)

    for n in range(1, len(TRANSFORMATIONS) + 1):
        for pool in itertools.permutations(TRANSFORMATIONS, n):
            out = copy.deepcopy(tile)
            for t in pool:
                out = t(out)
            if properly_oriented(out, *neighbors):
                return out
    raise ValueError("No valid transformation found")


def align_grid(tiles: dict[int, Tile]) -> list[list[Tile]]:
    side_length = int(math.sqrt(len(tiles)))
    out = [[None for _ in range(side_length)] for __ in range(side_length)]
    grid = place_tiles(tiles)

    # First, we need to deal with the top left corner. This will then lock us
    # in from there on out.
    tl = tiles[grid[0][0]]  # Top left
    b = tiles[grid[1][0]]  # Bottom
    r = tiles[grid[0][1]]  # Right
    # This won't necessarily be hyper-efficient, but it'll be work. I'd rather
    # it be right than clever.
    # First, we get the edges properly aligned.
    # Let's deal with the bottom side first
    tl_t, _, tl_l, tl_r = get_edge_differences(tl)
    b_edges = get_edge_differences(b)
    if tl_t in b_edges:
        tl = flip_over_x(tl)
    elif tl_l in b_edges:
        tl = flip_over_x(rotate_clockwise(tl))
    elif tl_r in b_edges:
        tl = rotate_clockwise(tl)

    # Now, we deal with the right side. The bottom is locked in, so we need it
    # to stay in the position it's in. The only possible sides that can match
    # the right-side tile are the left and right edges, and if it's already on
    # the right, we can do nothing.
    _, _, tl_l, _ = get_edge_differences(tl)
    r_edges = get_edge_differences(r)
    if tl_l in r_edges:
        tl = flip_over_y(tl)
    # The top left tile is now oriented. We can now zig-zag through the rest of
    # the tiles and orient them.
    out[0][0] = tl

    # Let's orient the top row.
    for x in range(1, side_length):
        out[0][x] = orient_tile(tiles[grid[0][x]], left=out[0][x - 1])

    # And now, for each remaining row, we orient the first tile, then the rest
    # of the row.
    for y in range(1, side_length):
        out[y][0] = orient_tile(tiles[grid[y][0]], top=out[y - 1][0])
        for x in range(1, side_length):
            out[y][x] = orient_tile(tiles[grid[y][x]],
                                    top=out[y - 1][x],
                                    left=out[y][x - 1])

    return out


def remove_borders(tile: Tile) -> Tile:
    topless = tile[1:]
    bottomless = topless[:-1]
    leftless = [row[1:] for row in bottomless]
    rightless = [row[:-1] for row in leftless]
    return rightless


def smoosh(grid: list[list[Tile]]) -> Tile:
    trimmed = [[remove_borders(tile) for tile in row] for row in grid]
    out = []
    for big_row in trimmed:
        n_little_rows = len(big_row[0])
        for i in range(n_little_rows):
            row = []
            for tile in big_row:
                row += tile[i]
            out.append(row)
    return out


def count_sea_monsters(grid: Tile) -> int:
    grid = ["".join(row) for row in grid]
    out = 0
    top_row_regex = re.compile(r".{18}#.")
    middle_row_regex = re.compile(r"#.{4}##.{4}##.{4}###")
    bottom_row_regex = re.compile(r"(.#.){6}..")
    # We'll start by looking for the middle row, since that seems like the
    # least likely to show up.
    for i, row in enumerate(grid[1:-1], start=1):
        if middle_match := re.search(middle_row_regex, row):
            # Check the coordinates of the rows right below and above
            start, end = middle_match.start(), middle_match.end()
            if not re.match(bottom_row_regex, grid[i + 1][start:end]):
                continue
            if not re.match(top_row_regex, grid[i - 1][start:end]):
                continue
            out += 1
            # # In case there are multiple in one row
            while True:
                if middle_match := re.search(middle_row_regex, row[end:]):
                    # Check the coordinates of the rows right below and above
                    start = middle_match.start() + end
                    end = middle_match.end() + end
                    if not re.match(bottom_row_regex, grid[i + 1][start:end]):
                        continue
                    if not re.match(top_row_regex, grid[i - 1][start:end]):
                        continue
                    out += 1
                else:
                    break

    return out


def transform_until_monsters_appear(grid: list[str]) -> int:
    if count := count_sea_monsters(grid):
        return count
    for transformation in set(TRANSFORMATIONS):
        if count := count_sea_monsters(transformation(grid)):
            return count

    for n in range(1, len(TRANSFORMATIONS) + 1):
        for pool in itertools.permutations(TRANSFORMATIONS, n):
            out = copy.deepcopy(grid)
            for t in pool:
                out = t(out)
            if count := count_sea_monsters(out):
                return count
    raise ValueError("No valid transformation found")


def roughness(grid: list[str]) -> int:
    n_monsters = transform_until_monsters_appear(grid)
    n_pounds = pretty_print(grid).count("#")
    return n_pounds - 15*n_monsters


def run(data: dict[int, Tile]) -> int:
    return roughness(smoosh(align_grid(data)))


def test():
    test_data = load_data(TEST_PATH)
    assert run(test_data) == 273


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    # test()
    main()
