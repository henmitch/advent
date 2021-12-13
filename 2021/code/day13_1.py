"""https://adventofcode.com/2021/day/13"""
import day13_0 as old


def main():
    points, folds = old.load_data(old.DATA_PATH)
    print(old.pretty_print(old.fold(points, folds)))


if __name__ == "__main__":
    main()
