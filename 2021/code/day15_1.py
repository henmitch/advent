"""https://adventofcode.com/2021/day/15"""
import heapq

import day15_0 as old


def load_data(path: str) -> old.Grid:
    return mult(old.load_data(path))


def cost(loc: old.Point, grid: old.Grid, size: int = 5) -> int:
    x, y = loc
    x_max, y_max = old.bottom_right(grid)
    x_max, y_max = x_max + 1, y_max + 1
    if x >= size*x_max or y >= size*y_max:
        return float("inf")
    # This is rather ugly.
    return ((grid[y%y_max][x%x_max] - 1) + x//x_max + y//y_max)%9 + 1


def mult(grid: old.Grid, size: int = 5) -> old.Grid:
    x_max = len(grid[0])*size - 1
    y_max = len(grid)*size - 1
    return tuple(
        tuple(cost((x, y), grid, size) for x in range(x_max + 1))
        for y in range(y_max + 1))


def a_star(grid: old.Grid,
           start: old.Point = (0, 0),
           end: old.Point = None) -> int:
    # We're gonna try to optimize this a bit, because size matters.
    # Now I'm REALLY flying by the seat of my pants.
    if end is None:
        end = old.bottom_right(grid)

    to_review = [(0, start)]

    so_far = {start: 0}

    while to_review:
        _, loc = heapq.heappop(to_review)
        if loc == end:
            return so_far[loc]

        for adjacent, cost in old.adjacents(grid, loc):
            new_cost = so_far[loc] + cost
            if adjacent not in so_far or new_cost < so_far[adjacent]:
                so_far[adjacent] = new_cost
                d = old.dist(grid, adjacent, end)
                heapq.heappush(to_review, (new_cost + d, adjacent))


def test():
    data = load_data(old.TEST_PATH)
    assert a_star(data) == 315


if __name__ == "__main__":
    test()
    data = load_data(old.DATA_PATH)
    print(a_star(data))
