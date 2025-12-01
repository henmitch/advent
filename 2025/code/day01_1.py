"""https://adventofcode.com/2025/day/1"""
import boilerplate as bp
from day01_0 import DATA_PATH, TEST_PATH, load_data


def run(data: tuple[int]) -> int:
    val = 50
    out = 0
    for num in data:
        plus, new_val = divmod(val + num, 100)
        if plus <= 0 == new_val:
            plus -= 1
        if plus < 0 == val:
            plus += 1
        plus = abs(plus)
        out += plus
        val = new_val
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 6


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
