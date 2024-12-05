"""https://adventofcode.com/2024/day/05"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

Ruleset = dict[int, tuple[set[int], set[int]]]
Pages = tuple[int, ...]


def load_data(path: str) -> tuple[Ruleset, list[Pages]]:
    with open(path, "r") as f:
        rules, pages = f.read().split("\n\n")
    rules = rules.splitlines()
    pages = pages.splitlines()

    return parse_rules(rules), parse_pages(pages)


def parse_rules(rules: list[str]) -> Ruleset:
    out = {}
    empty = (set(), set())
    for rule in rules:
        a, b = (map(int, rule.split("|")))
        a_rules = out.get(a, empty)
        b_rules = out.get(b, empty)
        out[a] = (a_rules[0] | {b}, a_rules[1])
        out[b] = (b_rules[0], b_rules[1] | {a})
    return out


def parse_pages(pageses: list[str]) -> list[Pages]:
    return [tuple(map(int, pages.split(","))) for pages in pageses]


def is_legal(rules: Ruleset, pages: Pages) -> bool:
    for i, page in enumerate(pages[:-1]):
        before, after = set(pages[:i]), set(pages[i + 1:])
        rule = rules.get(page, (set(), set()))
        if rule[0] & before or rule[1] & after:
            return False
    return True


def run(data: tuple[Ruleset, list[tuple[int, ...]]]) -> int:
    rules, pageses = data
    out = 0
    for pages in pageses:
        if is_legal(rules, pages):
            out += pages[len(pages)//2]

    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 143


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
