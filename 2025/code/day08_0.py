"""https://adventofcode.com/2025/day/8"""
import itertools

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

Triplet = tuple[int, int, int]


def load_data(path: str) -> list[Triplet]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return [tuple(int(x) for x in line.split(",")) for line in raw]


def find_all_dists(boxes: list[Triplet]) -> list[tuple[int, Triplet, Triplet]]:
    out = []
    for a, b in itertools.combinations(boxes, 2):
        # We don't need to square root because who cares about actual distance?
        # We only care about the order
        dist = sum((ai - bi)**2 for ai, bi in zip(a, b))
        out.append((dist, a, b))
    return out


def run(data: list[Triplet], n: int = 1000) -> int:
    dists = find_all_dists(data)
    groups = {box: {box} for box in data}
    connections = 0
    for _, a, b in sorted(dists):
        connections += 1
        if connections > n:
            break
        if a in groups[b]:
            continue
        new_group = groups[a] | groups[b]
        for loc in new_group:
            groups[loc] = new_group
    final_groups = sorted({frozenset(group)
                           for group in groups.values()},
                          key=len,
                          reverse=True)

    return len(final_groups[0])*len(final_groups[1])*len(final_groups[2])


def test():
    data = load_data(TEST_PATH)
    assert run(data, 10) == 40


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
