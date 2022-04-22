"""https://adventofcode.com/2020/day/23"""


def load_data(data: str):
    return [int(val) for val in data]


def get_destination(data: list[int], current: int, selected: list[int]) -> int:
    destination = current - 1
    while True:
        if destination not in data:
            destination = max(data)
        if destination in selected:
            destination -= 1
        else:
            return destination


def get_selected(data: list[int]) -> list[int]:
    return [data[val%len(data)] for val in range(1, 4)]


def rotate(lst: list, idx: int) -> list:
    return lst[idx + 1:] + lst[:idx + 1]


def step(data: list[int]) -> list[int]:
    current = data[0]
    selected = get_selected(data)
    destination = get_destination(data, current, selected)
    destination_idx = data.index(destination)
    out = [destination] + selected + [
        val for val in data[destination_idx + 1:] if val not in selected
    ] + [val for val in data[:destination_idx] if val not in selected]
    current_idx = out.index(current)
    return rotate(out, current_idx)


def finalize(lst: list[int]) -> list[int]:
    return rotate(lst, lst.index(1))


def run(cups: str) -> str:
    data = load_data(cups)
    for _ in range(100):
        data = step(data)
    return "".join(str(val) for val in finalize(data)[:-1])


def test():
    assert run("389125467") == "67384529"


def main():
    print(run("284573961"))


if __name__ == "__main__":
    test()
    main()
