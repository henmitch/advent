"""https://adventofcode.com/2023/day/15"""
from day15_0 import DATA_PATH, TEST_PATH, hashify, load_data


def split(line: str) -> tuple[str, int | None]:
    if line[-1] == "-":
        return line[:-1], None
    out = line.split("=")
    return out[0], int(out[1])


def hashmap(lines: list[str]) -> list[tuple[str, int]]:
    out = [[] for _ in range(256)]
    for line in lines:
        l, r = split(line)
        idx = hashify(l)
        if r is None:
            out[idx] = [v for v in out[idx] if v[0] != l]
            continue

        new_box = []
        replaced = False
        for label, val in out[idx]:
            if label == l:
                new_box.append((l, r))
                replaced = True
            else:
                new_box.append((label, val))
        if not replaced:
            new_box.append((l, r))
        out[idx] = new_box

    return out


def score(boxes: list[tuple[str, int]]) -> int:
    out = 0
    for i, box in enumerate(boxes):
        for j, pair in enumerate(box):
            out += (i + 1)*(j + 1)*pair[1]
    return out


def run(data: list[str]) -> int:
    return score(hashmap(data))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 145


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
