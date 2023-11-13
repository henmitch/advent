"""https://adventofcode.com/2022/day/20"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[int]:
    with open(path, "r") as f:
        raw = list(map(int, f.read().splitlines()))
    return raw


def run(base: list[int]) -> int:
    data = list(enumerate(base.copy()))
    for idx, val in enumerate(base):
        if not val:
            continue
        # The current index of `val` in `data`
        i = [j for j, pair in enumerate(data) if pair[0] == idx][0]
        data = data[i:] + data[:i]

        mod = (abs(val) + 1)%len(data)
        new_idx = mod + int(abs(val) > len(data))
        if val > 1:
            data = data[1:new_idx] + [data[0]] + data[new_idx:]
        elif val == 1:
            data = [data[1], data[0]] + data[2:]
        else:
            data = list(reversed(data))
            data = [data[-1]] + data[:-1]
            data = data[1:new_idx] + [data[0]] + data[new_idx:]
            data = list(reversed(data))

    zero_idx = [j for j, pair in enumerate(data) if pair[1] == 0][0]
    data = data[zero_idx:] + data[:zero_idx]
    return sum(data[n%len(data)][1] for n in [1000, 2000, 3000])


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 3


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
