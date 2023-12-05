"""https://adventofcode.com/2023/day/5"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class Mappings:

    def __init__(self, nums: list[tuple[int, int, int]]) -> None:
        self.mappings = nums

    def map_(self, num: int) -> int:
        for to, start, l in self.mappings:
            if start <= num < start + l:
                return to + (num - start)
        return num

    def start_endpoints(self) -> list[int]:
        return sorted((start, start + l - 1) for _, start, l in self.mappings)

    def end_endpoints(self) -> list[int]:
        return [(to, to + l - 1) for to, _, l in self.mappings]


def load_data(path: str) -> tuple[list[int], list[list[Mappings]]]:
    with open(path, "r") as f:
        raw = f.read().split("\n\n")
    raw_seeds, *raw_mappingses = raw

    seeds = list(map(int, raw_seeds.split(": ")[1].split()))

    mappingses = []
    for mappings in raw_mappingses:
        mappings = mappings.splitlines()[1:]
        mappings = [list(map(int, line.split())) for line in mappings]
        mappingses.append(Mappings(mappings))

    return seeds, mappingses


def run(data: tuple[list[int], list[Mappings]]) -> int:
    outs = []
    ns, mappingses = data
    for n in ns:
        current = n
        for mappings in mappingses:
            current = mappings.map_(current)
        outs.append(current)
    out = min(outs)
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 35


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
