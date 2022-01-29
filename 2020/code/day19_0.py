"""https://adventofcode.com/2020/day/19"""
import itertools
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[dict[str, str], set[str]]:
    with open(path, "r") as f:
        rules, vals = f.read().split("\n\n")
    rules = {
        rule.split(": ")[0]: rule.split(": ")[1].replace("\"", "")
        for rule in rules.split("\n")
    }
    vals = set(vals.split("\n"))
    return rules, vals


def parse(num: str, rules: dict[str, str]) -> set[str]:
    val = rules[num]
    if val in {"a", "b"}:
        return {val}
    splitted = val.split("|")
    out = set()
    for part in splitted:
        for next_strs in itertools.product(
                *map(lambda x: parse(x, rules), part.split())):
            out.add("".join(next_strs))
    return out


def run(rules: dict[str, str], vals: set[str]) -> int:
    valid = parse("0", rules)
    return len(valid & vals)


def test():
    rules, vals = load_data(TEST_PATH)
    assert run(rules, vals) == 3


def main():
    rules, vals = load_data(DATA_PATH)
    print(run(rules, vals))


if __name__ == "__main__":
    test()
    main()
