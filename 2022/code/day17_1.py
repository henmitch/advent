"""https://adventofcode.com/2022/day/17"""
from itertools import cycle

from day17_0 import (DATA_PATH, SHAPES, TEST_PATH, Block, load_data,
                     max_height, pretty_print, top_boundary)


def cycle_data(data: list[str],
               n_blocks: int = 2022) -> tuple[int, int, int, int]:
    space = set()
    moves = cycle(zip(data, range(len(data))))
    shapes = cycle(zip(SHAPES.keys(), range(len(SHAPES))))
    starting_pairs = {}
    seen_all_moves = False
    for block_number in range(n_blocks):
        next_shape, shape_idx = next(shapes)
        block = Block(next_shape, 2 + (max_height(space) + 3)*1j)
        while True:
            next_move, move_idx = next(moves)
            # If we reach the beginning of our list of moves for the second
            # time, then we've seen all the moves
            if not seen_all_moves and move_idx == len(data) - 1:
                seen_all_moves = True
            if not block.move(next_move, space):
                break
        space = space | block.points
        # space = top_boundary(space | block.points)
        # Stop if we get back to the beginning
        pair = (shape_idx, move_idx)
        current = starting_pairs.get(pair, [])
        if seen_all_moves and len(current) == 3:
            break
        starting_pairs[pair] = current + [(block_number, max_height(space))]
    else:
        return n_blocks, max_height(space)
    # the period of the periodic bit,
    l_period = current[-1][0] - current[-2][0]
    # the height of each period of the periodic bit
    h_period = current[-1][1] - current[-2][1]
    return (l_period, h_period)


def play(data: list[str], n_blocks: int = 2022) -> int:
    space = set()
    data = cycle(data)
    shapes = cycle(SHAPES.keys())
    for _ in range(n_blocks):
        block = Block(next(shapes), 2 + (max_height(space) + 3)*1j)
        while block.move(next(data), space):
            pass
        space = space | block.points
        # space = top_boundary(space | block.points)
    # print(pretty_print(space, block))
    # print(7*"-")
    return max_height(space)


def run(data: list[str], n_blocks: int = 2022) -> int:
    # Height will be number of cycles * height of cycle + height of remainder
    l_period, h_period = cycle_data(data, n_blocks)
    print(f"Blocks per cycle: {l_period}")
    print(f"Height per cycle: {h_period}")
    n_cycles, blocks_remain = divmod(n_blocks, l_period)
    print(f"Sanity check: {n_cycles*l_period + blocks_remain}")
    print(f"Number of cycles: {n_cycles}")
    print(f"Remaining blocks: {blocks_remain}")
    # Go through l_pre steps and then remove their height
    remaining_height = play(data, blocks_remain)
    print(f"Remaining height: {remaining_height}")
    total_height = n_cycles*h_period + remaining_height
    print(f"Total height: {total_height}")
    print()
    return total_height


def test():
    data = load_data(TEST_PATH)
    out = run(data, 1000000000000)
    assert out == 1514285714288
    assert run(data) == 3068


def main():
    data = load_data(DATA_PATH)
    assert run(data) == 3171
    print(run(data, 1000000000000))


if __name__ == "__main__":
    test()
    main()
