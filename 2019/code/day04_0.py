"""https://adventofcode.com/2019/day/4"""
Pair = tuple[int, int]


def valid(val: int) -> bool:
    val = split_into_pairs(val)
    if not all(increasing(pair) for pair in val):
        return False
    return any(repeating(pair) for pair in val)


def split_into_pairs(val: int) -> tuple[Pair, ...]:
    val = str(val)
    return tuple(zip(val[:-1], val[1:]))


def increasing(pair: Pair) -> bool:
    return pair[1] >= pair[0]


def repeating(pair: Pair) -> bool:
    return pair[0] == pair[1]


def make_range(vals: str) -> range:
    dash = vals.index("-")
    start, stop = int(vals[:dash]), int(vals[dash + 1:])
    if start < 1e5 or stop >= 1e6:
        raise ValueError("Values must be 6-digit")
    return range(start, stop + 1)


def count_in_range(vals: range) -> int:
    return sum(valid(val) for val in vals)


def run(vals: str) -> int:
    return count_in_range(make_range(vals))


def test():
    assert valid(111111)
    assert not valid(223450)
    assert not valid(123789)


def main():
    print(run("254032-789860"))


if __name__ == "__main__":
    test()
    main()
