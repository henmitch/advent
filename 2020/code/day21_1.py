"""https://adventofcode.com/2020/day/21"""
import day21_0 as old


def run(pairings: tuple[old.Pairing]) -> str:
    ingredients = []
    mapping = old.find_mapping(pairings)
    for allergen in sorted(mapping):
        ingredients += list(mapping[allergen])
    return ",".join(ingredients)


def test():
    test_data = old.load_data(old.TEST_PATH)
    assert run(test_data) == "mxmxvkd,sqjhc,fvjkl"


def main():
    data = old.load_data(old.DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
