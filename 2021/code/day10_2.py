"""https://adventofcode.com/2021/day/10

Stack time!
"""
import re
from typing import List, Tuple

import boilerplate as bp

DATA_PATH = bp.get_data_path()
TEST_PATH = bp.get_test_path()

VALID_PAIRS = re.compile(r"(?:\(\)|\{\}|\[\]|<>)")
PAIRINGS = {")": "(", "}": "{", "]": "[", ">": "<"}
OPENERS = set(PAIRINGS.values())
CLOSERS = set(PAIRINGS.keys())

INVALID_SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}
AUTOCOMPLETE_SCORES = {"(": 1, "[": 2, "{": 3, "<": 4}


def load_data(path):
    """Load data from file"""
    with open(path, "r") as f:
        return f.read().splitlines()


def get_score(row: List[str]) -> Tuple[int, bool]:
    """Returns the score and whether the line is valid"""
    stack = []
    for char in row:
        # print("".join(stack), char)
        if char in OPENERS:
            stack.append(char)
        elif char in CLOSERS:
            # Invalid
            if not stack or stack.pop() != PAIRINGS[char]:
                score = INVALID_SCORES[char]
                return score, False

    # Autocomplete
    score = 0
    for char in stack[::-1]:
        score *= 5
        score += AUTOCOMPLETE_SCORES[char]
    return score, True


def main():
    data = load_data(DATA_PATH)
    scores = [get_score(row) for row in data]
    invalids = []
    autos = []
    for score, valid in scores:
        if not valid:
            invalids.append(score)
        else:
            autos.append(score)
    autos = sorted(autos)[len(autos)//2]
    print(f"Part 1: {sum(invalids)}")
    print(f"Part 2: {autos}")


if __name__ == "__main__":
    main()
