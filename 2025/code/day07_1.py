"""https://adventofcode.com/2025/day/1"""
import boilerplate as bp
from day07_0 import DATA_PATH, TEST_PATH, load_data


def run(data: str) -> int:
    current = {data[0].index("S")}
    paths = [0]*len(data[0])
    paths[data[0].index("S")] = 1
    for row in data[1:]:
        next_ = set()
        for j, val in enumerate(row):
            if j in current:
                if val == "^":
                    next_ |= {j - 1, j + 1}
                    paths[j - 1] += paths[j]
                    paths[j + 1] += paths[j]
                    paths[j] = 0
                else:
                    next_ |= {j}
        current = next_

    return sum(paths)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 40


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
