"""https://adventofcode.com/2021/day/20"""
from typing import List, Tuple

import boilerplate as bp

Image = List[List[str]]

DATA_PATH = bp.get_data_path()
TEST_PATH = bp.get_test_path()


def load_data(path: str) -> Tuple[Image, str]:
    with open(path, "r") as f:
        raw = f.read()
    alg, data = raw.split("\n\n")
    img = [list(row) for row in data.split("\n")]
    # We pad by 2 to make sure we cover the edges
    return pad(img, 2), alg


def pad(img: Image, n: int = 3, padder: str = ".") -> Image:
    width = len(img[0])
    new_width = width + 2*n
    blank_rows = [list(padder*new_width) for _ in range(n)]
    return blank_rows + [list(padder*n) + row + list(padder*n)
                         for row in img] + blank_rows


def pixel_to_binary(img: Image, x: int, y: int) -> str:
    out = ""
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if img[y + dy][x + dx] == "#":
                out += "1"
            else:
                out += "0"
    return out


def pixel_to_int(img: Image, x: int, y: int) -> int:
    return int(pixel_to_binary(img, x, y), 2)


def enhance(img: Image, alg: str, padder: str = ".") -> Image:
    img = pad(img, padder=padder, n=2)
    out = []
    for y, row in enumerate(img[1:-1]):
        row_out = ""
        for x, _ in enumerate(row[1:-1]):
            row_out += alg[pixel_to_int(img, x + 1, y + 1)]
        out.append(list(row_out))
    return out


def n_illuminated(img: Image) -> int:
    return sum(1 for row in img for px in row if px == "#")


def process(img: Image, alg: str) -> int:
    img = enhance(img, alg)
    filler = alg[0]
    img = enhance(img, alg, filler)
    return n_illuminated(img)


def pretty_print(img):
    print("\n".join(["".join(row) for row in img]))


def test():
    data = load_data(TEST_PATH)
    assert process(*data) == 35


def main():
    data = load_data(DATA_PATH)
    print(process(*data))


if __name__ == "__main__":
    test()
    main()
