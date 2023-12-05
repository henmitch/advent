"""https://adventofcode.com/2023/day/5"""
from day05_0 import DATA_PATH, TEST_PATH, Mappings, load_data

Pair = tuple[int, int]


def run(data: tuple[list[int], list[Mappings]]) -> int:
    ns, mappingses = data
    care_about_now = sorted([(ns[i], ns[i] + ns[i + 1] - 1)
                             for i in range(0, len(ns), 2)])
    for mappings in mappingses:
        map_endpoints = mappings.start_endpoints()
        care_about_now = breakup(care_about_now, map_endpoints)
        care_about_next = []
        for lower, upper in care_about_now:
            if mappings.map_(lower) > mappings.map_(upper):
                raise ValueError(f"{lower=}, {upper=}")
            care_about_next.append(
                (mappings.map_(lower), mappings.map_(upper)))

        care_about_now = care_about_next
    return min(care_about_now)[0]


def breakup(range_endpointses: list[Pair],
            mapping_endpointses: list[Pair]) -> list[Pair]:
    out = []
    for endpoints in range_endpointses:
        start, end = endpoints
        overlappers = [m for m in mapping_endpointses if overlap(endpoints, m)]
        if not overlappers:
            out.append(endpoints)
            continue
        # Trimming so we can ignore overhang
        overlappers[0] = (max(overlappers[0][0], start), overlappers[0][1])
        overlappers[-1] = (overlappers[-1][0], min(overlappers[-1][1], end))
        if start < overlappers[0][0]:
            out.append((start, overlappers[0][0] - 1))
        out.append(overlappers[0])
        # Add the rest
        for overlapper in overlappers[1:]:
            if out[-1][1] + 1 <= overlapper[0] - 1:
                out.append((out[-1][1] + 1, overlapper[0] - 1))
            out.append(overlapper)
        # If we still have more to do, do it
        if out[-1][1] < end:
            out.append((out[-1][1] + 1, end))
    return sorted(set(out))


def overlap(a: Pair, b: Pair) -> bool:
    # NOTE that this doesn't account for b completely enveloping a
    return a[0] <= b[0] <= a[1] or a[0] <= b[1] <= a[1]


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 46


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
