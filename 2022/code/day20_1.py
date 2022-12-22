"""https://adventofcode.com/2022/day/20"""
from day20_0 import TEST_PATH, DATA_PATH, load_data


def run(base: list[int], key: int = 811589153) -> int:
    new_base = [i*key for i in base]
    data = list(enumerate(new_base))
    for _ in range(10):
        for idx, val in enumerate(new_base):
            if not val:
                continue
            # The current index of `val` in `data`
            i = [j for j, pair in enumerate(data) if pair[0] == idx][0]
            data = data[i:] + data[:i]

            mod = (abs(val))%(len(data) - 1)
            new_idx = mod + int(abs(val) > len(data))
            if val > 1:
                data = data[1:new_idx] + [data[0]] + data[new_idx:]
            elif val == 1:
                data = [data[1], data[0]] + data[2:]
            else:
                data = list(reversed(data))
                data = [data[-1]] + data[:-1]
                data = data[1:new_idx] + [data[0]] + data[new_idx:]
                data = list(reversed(data))

    zero_idx = [j for j, pair in enumerate(data) if pair[1] == 0][0]
    data = data[zero_idx:] + data[:zero_idx]
    return sum(data[n%len(data)][1] for n in [1000, 2000, 3000])


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 1623178306
    # print(run([0, 4, 5, 1, 2, 3]))


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
