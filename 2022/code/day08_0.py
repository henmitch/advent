"""https://adventofcode.com/2022/day/8"""
from functools import reduce
from operator import or_

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> list[list[int]]:
    with open(path, "r") as f:
        data = list(map(list, f.read().splitlines()))
    for i, row in enumerate(data):
        data[i] = list(map(int, row))
    return data


def visible_from_top(data: list[list[int]]) -> list[list[bool]]:
    out = [len(data[0])*[True]]
    max_so_far = data[0].copy()
    for row in data[1:]:
        new_row = []
        for j, value in enumerate(row):
            new_row.append(max_so_far[j] < value)
            max_so_far[j] = max(max_so_far[j], value)
        out.append(new_row)
    return out


def visible_from_bottom(data: list[list[int]]) -> list[list[bool]]:
    out = [len(data[0])*[True]]
    max_so_far = data[-1].copy()
    for row in data[-2::-1]:
        new_row = []
        for j, value in enumerate(row):
            new_row.append(max_so_far[j] < value)
            max_so_far[j] = max(max_so_far[j], value)
        out.insert(0, new_row)
    return out


def visible_from_left(data: list[list[int]]) -> list[list[bool]]:
    out = []
    max_so_far = [row[0] for row in data]
    for i, row in enumerate(data):
        new_row = [True]
        for value in row[1:]:
            new_row.append(max_so_far[i] < value)
            max_so_far[i] = max(max_so_far[i], value)
        out.append(new_row)
    return out


def visible_from_right(data: list[list[int]]) -> list[list[bool]]:
    out = []
    max_so_far = [row[-1] for row in data]
    for i, row in enumerate(data):
        new_row = [True]
        for value in row[-2::-1]:
            new_row.insert(0, max_so_far[i] < value)
            max_so_far[i] = max(max_so_far[i], value)
        out.append(new_row)
    return out


def and_all(*datas) -> list[list[bool]]:
    n_rows, n_columns = len(datas[0]), len(datas[0][0])
    out = []
    for i in range(n_rows):
        new_row = []
        for j in range(n_columns):
            new_row.append(reduce(or_, (data[i][j] for data in datas)))
        out.append(new_row)
    return out


def pretty_print(data: list[list[bool]]) -> None:
    for row in data:
        print("".join(str(int(val)) for val in row))


def count_total(data: list[list[bool]]) -> int:
    return sum(sum(row) for row in data)


def run(data: list[list[int]]) -> int:
    t = visible_from_top(data)
    b = visible_from_bottom(data)
    l = visible_from_left(data)
    r = visible_from_right(data)
    return count_total(and_all(t, b, l, r))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 21


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
