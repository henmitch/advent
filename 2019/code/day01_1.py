"""https://adventofcode.com/2019/day/1"""
import boilerplate as bp

DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[int]:
    with open(path, "r") as f:
        return tuple(int(i) for i in f.readlines())


def fuel(mass: int) -> int:
    out = int(mass/3) - 2
    marginal = out
    while marginal > 0:
        marginal = int(marginal/3) - 2
        out += max(marginal, 0)
    return out


def total_fuel(masses: tuple[int, ...]) -> int:
    return sum(fuel(mass) for mass in masses)


def main():
    data = load_data(DATA_PATH)
    print(total_fuel(data))


if __name__ == "__main__":
    main()
