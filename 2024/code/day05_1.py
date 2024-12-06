"""https://adventofcode.com/2024/day/5"""
import boilerplate as bp
from day05_0 import DATA_PATH, TEST_PATH, Pages, Ruleset, is_legal, load_data


def legalize(rules: Ruleset, pages: Pages) -> Pages:
    stripped = {}
    for page in pages:
        first, second = rules[page]
        pages_set = set(pages)
        stripped[page] = first & pages_set, second & pages_set
    out = sorted(stripped, key=lambda x: len(stripped[x][1]))
    return out


def run(data: tuple[Ruleset, list[Pages]]) -> int:
    rules, pageses = data
    out = 0
    for pages in pageses:
        if not is_legal(rules, pages):
            out += legalize(rules, pages)[len(pages)//2]

    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 123


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
