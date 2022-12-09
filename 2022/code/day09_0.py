"""https://adventofcode.com/2022/day/9"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

DIRECTIONS = {
    "U": 0 + 1j,
    "D": 0 - 1j,
    "L": -1 + 0j,
    "R": 1 + 0j,
}


def load_data(path: str) -> list[tuple[str, int]]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    data = [line.split() for line in raw]
    return [(x[0], int(x[1])) for x in data]


def move(instruction: tuple[str, int],
         head: complex = 0,
         tail: complex = 0) -> tuple[tuple[complex, complex], set[complex]]:
    direction = DIRECTIONS[instruction[0]]
    distance = instruction[1]
    out = {tail}
    # How many steps we take before moving the tail
    stop_early = 0
    # We want to take steps until the head is generally in the direction that
    # the rope is going, to handle cases like the following:
    # .T..  .T..  .T..  ....
    # H...  .H..  ..H.  ..TH
    if head == tail:
        pass
    elif direction.imag == 0:  # Going L or R
        while (head - tail).real != direction.real and stop_early < distance:
            head += direction
            stop_early += 1
    elif direction.real == 0:  # Going U or D
        while (head - tail).imag != direction.imag and stop_early < distance:
            head += direction
            stop_early += 1
    for _ in range(distance - stop_early):
        tail = head
        head += direction
        out.add(tail)
    if abs((head - tail).imag) > 1 or abs((head - tail).real) > 1:
        raise ValueError(f"Head and tail too far apart")
    return (head, tail), out


def run(data: list[tuple[str, int]]) -> int:
    head = tail = 0
    out = {0}
    for row in data:
        (head, tail), to_add = move(row, head, tail)
        out |= to_add
    return len(out)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 13


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
