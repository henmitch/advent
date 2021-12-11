"""https://adventofcode.com/2021/day/4"""
import os
import re
from typing import List

Board = List[List[int]]

data_dir = os.path.join(os.path.dirname(__file__), "data")
PATH = os.path.join(data_dir, "day04_0.txt")


def load_data(path):
    with open(path, "r") as f:
        data = f.read().split("\n\n")

    numbers = [int(x) for x in data[0].split(",")]
    # Turning the boards into a list of lists of lists
    boards = []
    for board in data[1:]:
        boards.append([[int(x) for x in re.compile("\s+").split(row.strip())]
                       for row in board.split("\n")])
    return numbers, boards


def has_bingo(board: Board) -> bool:
    """Check if a board has bingo"""
    # Check rows
    if any(all(x is None for x in row) for row in board):
        return True
    # Check columns
    if any(all(x is None for x in col) for col in zip(*board)):
        return True
    return False


def place_number(number: int, boards: List[Board]) -> List[Board]:
    """Play a number on all boards"""
    for board in boards:
        for row in board:
            for i, num in enumerate(row):
                if num == number:
                    row[i] = None
    return boards


def score_board(board: Board, last_number: int) -> int:
    """Score a board"""
    score = 0
    for row in board:
        for num in row:
            if num is not None:
                score += num
    return score*last_number


def play_to_win(numbers: List[int], boards: List[Board]) -> int:
    """Play the game"""
    last_number = None
    while True:
        last_number = numbers.pop(0)
        boards = place_number(last_number, boards)
        for board in boards:
            if has_bingo(board):
                return score_board(board, last_number)


def main():
    numbers, boards = load_data(PATH)
    print(play_to_win(numbers, boards))


if __name__ == "__main__":
    main()
