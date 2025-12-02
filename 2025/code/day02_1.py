"""https://adventofcode.com/2025/day/2"""
from boilerplate import write_answer
from day02_0 import DATA_PATH, TEST_PATH, load_data


def generate_valids_of_width(range_: tuple[int, int], width: int) -> set[int]:
    start, end = range_
    out = set()
    for l in range(len(str(start)), len(str(end)) + 1):
        if l%width:
            continue
        base = "1" + "0"*(width - 1)
        while True:
            if l == width:
                break
            testing = int(base*(l//width))
            if testing > end:
                break
            if testing >= start:
                out.add(testing)
            base = str(int(base) + 1)
    return out


def generate_all_valids(range_: tuple[int, int]) -> set[int]:
    valids = set()
    l = len(str(range_[1]))
    for width in range(1, l//2 + 1):
        valids |= generate_valids_of_width(range_, width)
    return valids


def run(data: tuple[tuple[int, int], ...]) -> int:
    valids = set()
    for range_ in data:
        valids |= generate_all_valids(range_)
    return sum(valids)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 4174379265


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
