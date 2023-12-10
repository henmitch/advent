"""https://adventofcode.com/2023/day/10"""
import boilerplate as bp

TEST_PATH = bp.get_test_path("00")
DATA_PATH = bp.get_data_path()

PIPES = {
    "|": ("S", "N"),
    "-": ("E", "W"),
    "L": ("N", "E"),
    "J": ("W", "N"),
    "7": ("S", "W"),
    "F": ("E", "S")
}
DIRS = {"N": 0 - 1j, "E": 1 + 0j, "S": 0 + 1j, "W": -1 + 0j}
OPPOSITES = {"N": "S", "S": "N", "E": "W", "W": "E"}


def load_data(path: str) -> list[str]:
    with open(path, "r") as f:
        data = f.read().splitlines()
    return data


class Pipes:

    def __init__(self, data: list[str]) -> None:
        self.data = data
        self.width = len(data[0])
        self.height = len(data)
        self.start = self.get_starting_point()

    def __getitem__(self, loc: complex) -> str:
        if self.oob(loc):
            raise ValueError(f"{loc} is out of bounds")
        x, y = loc.real, loc.imag
        return self.data[int(y)][int(x)]

    def get_starting_point(self) -> complex:
        for i, line in enumerate(self.data):
            for j, char in enumerate(line):
                if char == "S":
                    return j + 1j*i
        raise NotImplementedError("Cannot analyze map without S")

    def oob(self, loc: complex) -> bool:
        if any(pt < 0 for pt in [loc.real, loc.imag]):
            return True
        if loc.imag >= self.height or loc.real >= self.width:
            return True
        return False

    def get_neighbors(self, loc: complex) -> set[complex]:
        out = []
        if self[loc] == "S":
            for dir_, step in DIRS.items():
                if self.oob(new_point := loc + step):
                    continue
                if self[new_point] not in PIPES:
                    continue
                if OPPOSITES[dir_] in PIPES[self[new_point]]:
                    out += [new_point]
            return set(out)

        dirs_pipe_goes = [
            step for dir_, step in DIRS.items() if dir_[0] in PIPES[self[loc]]
        ]
        for step in dirs_pipe_goes:
            if self.oob(new_point := loc + step):
                continue
            out += [new_point]
        return set(out)

    def walk(self) -> list[complex]:
        out = [self.start]
        current = self.get_neighbors(self.start).pop()  # Pick any direction
        while current != self.start:
            out.append(current)
            current = (self.get_neighbors(current) - {out[-2]}).pop()
        return out


def run(data: list[str]) -> int:
    cycle = Pipes(data).walk()
    return len(cycle)//2


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 8


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
