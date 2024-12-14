"""https://adventofcode.com/2024/day/14"""
import os

import boilerplate as bp
from day14_0 import DATA_PATH, DEFAULT_HEIGHT, DEFAULT_WIDTH, Robot, load_data


def pretty_print(data: list[Robot], width: int, height: int, t: int) -> int:
    grid = [[" " for _ in range(width)] for _ in range(height)]
    for bot in data:
        x, y = bot.position(t)
        grid[y][x] = "#"
    return "\n".join("".join(row) for row in grid)


def run(data: list[Robot]) -> int:
    t = 10403
    while True:
        pretty = pretty_print(data, DEFAULT_WIDTH, DEFAULT_HEIGHT, t)
        with open("day14_1_out.txt", "w") as f:
            f.write(f"t = {t}\n")
            f.write(pretty + "\n")
        print(pretty)
        if input("Is this a Christmas tree? (y/n): ").lower() == "y":
            os.remove("day14_1_out.txt")
            break
        t += 1
    return t


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    # This doesn't feel great, but I looked at the outputs, noticed a pattern
    # of high horizontal density with a specific starting point t_h and a
    # period of T_h, and a pattern of high vertical density with a another
    # specific starting point t_v and another period of T_v. I then found the
    # first point where (t - t_h) % T_h == (t - t_v) % T_v == 0.
    main()
