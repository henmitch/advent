"""You're already almost 1.5km (almost a mile) below the surface of the ocean,
already so deep that you can't see any sunlight. What you can see, however, is
a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers.
Numbers are chosen at random, and the chosen number is marked on all boards on
which it appears. (Numbers may not appear on all boards.) If all numbers in any
row or any column of a board are marked, that board wins. (Diagonals don't
count.)

The submarine has a bingo subsystem to help passengers (currently, you and th
 giant squid) pass the time. It automatically generates a random order in which
to draw numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no
winners, but the boards are marked as follows (shown here adjacent to each
other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are
still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
At this point, the third board wins because it has at least one complete row or
column of marked numbers (in this case, the entire top row is marked: 14 21 17
24 4).

The score of the winning board can now be calculated. Start by finding the sum
of all unmarked numbers on that board; in this case, the sum is 188. Then,
multiply that sum by the number that was just called when the board won, 24, to
get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win
first. What will your final score be if you choose that board?
"""
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
    return score * last_number


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
