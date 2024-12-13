"""https://adventofcode.com/2024/day/13"""
import boilerplate as bp
from day13_0 import DATA_PATH, TEST_PATH, Claw, load_data


def post_process(claw: Claw) -> Claw:
    xa, ya, xb, yb, xp, yp = claw
    return xa, ya, xb, yb, xp + 10000000000000, yp + 10000000000000


def solve(claw: Claw) -> tuple[int, int]:
    xa, ya, xb, yb, xp, yp = claw
    a = (xb*yp - xp*yb)/(xb*ya - xa*yb)
    b = (yp - a*ya)/yb
    return a, b


def run(data: list[Claw]) -> int:
    out = 0
    for claw in data:
        claw = post_process(claw)
        a, b = solve(claw)
        if a.is_integer() and b.is_integer():
            out += int(3*a + b)
    return out


def test():
    data = [post_process(claw) for claw in load_data(TEST_PATH)]
    assert not all(isinstance(v, int) for v in solve(data[0]))
    assert all(v.is_integer() for v in solve(data[1]))
    assert not all(isinstance(v, int) for v in solve(data[2]))
    assert all(v.is_integer() for v in solve(data[3]))


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    # test()
    main()
