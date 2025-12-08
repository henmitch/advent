"""https://adventofcode.com/2025/day/8"""
import boilerplate as bp
from day08_0 import DATA_PATH, TEST_PATH, load_data, find_all_dists, Triplet


def run(data: list[Triplet]) -> int:
    out = 0
    dists = find_all_dists(data)
    groups = {box: {box} for box in data}
    box_set = set(data)
    for _, a, b in sorted(dists):
        if a in groups[b]:
            continue
        new_group = groups[a] | groups[b]
        if new_group == box_set:
            return a[0]*b[0]
        for loc in new_group:
            groups[loc] = new_group

    raise RuntimeError("new_group never equaled box_set")


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 25272


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
