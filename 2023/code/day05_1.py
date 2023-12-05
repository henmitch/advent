"""https://adventofcode.com/2023/day/5"""
from day05_0 import DATA_PATH, TEST_PATH, Mappings, load_data


def run(data: tuple[list[int], list[Mappings]]) -> int:
    ns, mappingses = data
    care_about_now = [(ns[i], ns[i] + ns[i + 1] - 1)
                      for i in range(0, len(ns), 2)]
    for mappings in mappingses:
        care_about_next = []
        next_endpoints = mappings.start_endpoints()
        to_add = []
        for lower, upper in care_about_now:
            for lower_m, upper_m in next_endpoints:
                # If mapping entirely enclosed...
                if lower < lower_m and upper_m < upper:
                    # Break into 3
                    to_add += [(lower, lower_m-1), (lower_m, upper_m),
                               (upper_m+1, upper)]
                # If mapping contains upper bound...
                elif lower < lower_m < upper:
                    # Break into 2
                    to_add += [(lower, lower_m-1), (lower_m, upper)]
                # If mapping contains lower bound...
                elif lower < upper_m < upper:
                    # break into 2
                    to_add += [(lower, upper_m), (upper_m+1, upper)]
        care_about_now += to_add
        for lower, upper in care_about_now:
            care_about_next.append((mappings.map_(lower), mappings.map_(upper)))
        care_about_now = care_about_next
    return min(care_about_now)[0]


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 46


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
