"""https://adventofcode.com/2021/day/10"""
from typing import List

import day10_0 as old


def discard_corrupted_lines(data: List[str]) -> List[str]:
    """Discard corrupted lines from the input data."""
    corrupteds = old.find_all_invalid_chars(data)
    return [
        line for line, corrupted in zip(data, corrupteds) if corrupted == ""
    ]


def complete_line(line: str) -> str:
    """Complete a line, matching delimiters"""
    pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
    to_add = ""
    line = old.remove_valid(line)
    for char in line[::-1]:
        if char in pairs:
            to_add += pairs[char]

    return to_add


def complete_all_lines(data: List[str]) -> List[str]:
    """Complete all lines in the input data."""
    return [complete_line(line) for line in data]


def score_line(line: str) -> int:
    """Score a line."""
    score_map = {")": 1, "]": 2, "}": 3, ">": 4}
    score = 0
    for char in line:
        score *= 5
        score += score_map[char]
    return score


def score_data(data: List[str]) -> int:
    """Score the input data."""
    scores = sorted([score_line(line) for line in complete_all_lines(data)])
    return scores[len(scores)//2]


def test():
    data = discard_corrupted_lines(old.load_data(old.TEST_PATH))
    assert score_data(data) == 288957


if __name__ == "__main__":
    test()
    data = discard_corrupted_lines(old.load_data(old.DATA_PATH))
    print(score_data(data))
