"""https://adventofcode.com/2022/day/10"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def addx(x: int, v: int) -> list[int]:
    return [x, v + x]


def noop(x: int) -> list[int]:
    return [x]


def execute(data: list[str], n: int = -1) -> list[int]:
    out = [1]
    if n == -1:
        n = len(data)
    for line in data[:n]:
        x = out[-1]
        if line == "noop":
            out += noop(x)
        else:
            v = int(line.split()[1])
            out += addx(x, v)
    return out


def run(data: list[str]) -> int:
    out = 0
    nums = execute(data, n=220)
    for i in range(20, 260, 40):
        out += i*nums[i - 1]
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 13140


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
