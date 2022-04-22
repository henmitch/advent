"""https://adventofcode.com/2020/day/23"""

Cups = dict[int, tuple[int, int]]


def load_data(data: str):
    intermediate = [int(val) for val in data]
    out = intermediate + list(range(max(intermediate) + 1, int(1e6) + 1))
    return make_cups(out)


# The data is of the structure:
# {cup_number: (left_number, right_number),
#  cup_number: (left_number, right_number)}


def make_cups(nums: list[int]) -> Cups:
    out = {}
    # Separate this out to avoid index errors or taking len and modding.
    out[nums[-1]] = (nums[-2], nums[0])
    for i, num in enumerate(nums[:-1]):
        out[num] = (nums[i - 1], nums[i + 1])
    return out


def step(cups: Cups, current: int) -> tuple[Cups, int]:
    select = get_selected(cups, current)
    dest = get_destination(cups, current, select)
    cups[current] = (cups[current][0], cups[select[2]][1])
    after = cups[dest][1]
    cups[dest] = (cups[dest][0], select[0])
    cups[select[0]] = (dest, select[1])
    cups[select[1]] = (select[0], select[2])
    cups[select[2]] = (select[1], after)
    cups[after] = (select[2], cups[after][1])

    return cups, cups[current][1]


def get_selected(cups: Cups, current: int) -> tuple[int, int, int]:
    # Get the 3 cups to the right of the current cup
    return chain(cups, n=3, current=current)


def get_destination(cups: Cups, current: int, select: tuple[int, ...]) -> int:
    destination = current - 1
    while True:
        if destination not in cups:
            destination = max(cups)
        if destination in select:
            destination -= 1
        else:
            return destination


def chain(cups: Cups, n: int = None, current: int = None) -> str:
    if n is None:
        n = len(cups) - 1
    if current is None:
        current = 1
    out = []
    for _ in range(n):
        next_ = cups[current][1]
        out.append(next_)
        current = next_
    return out


def run(cups: str) -> int:
    current = int(cups[0])
    cups = load_data(cups)
    for _ in range(10_000_000):
        cups, current = step(cups, current)
    labels = chain(cups, 2)
    return labels[0]*labels[1]


def test():
    assert run("389125467") == 149245887792


def main():
    print(run("284573961"))


if __name__ == "__main__":
    # test()
    main()
