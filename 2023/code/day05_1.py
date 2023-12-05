"""https://adventofcode.com/2023/day/5"""
from day05_0 import DATA_PATH, TEST_PATH, Mappings, load_data


def run(data: tuple[list[int], list[Mappings]]) -> int:
    ns, mappingses = data
    care_about_now = [(ns[i], ns[i] + ns[i + 1] - 1)
                      for i in range(0, len(ns), 2)]
    for mappings in mappingses:
        care_about_next = []
        next_endpoints = mappings.start_endpoints()
        # TODO: Create new endpoints depending on overlap
        care_about_now = care_about_next
    return min(care_about_now)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 46


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
