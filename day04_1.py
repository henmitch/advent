"""--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant
squid win.

You aren't sure how many bingo boards a giant squid could play at once, so
rather than waste time counting its arms, the safe thing to do is to figure out
which board will win last and choose that one. That way, no matter which boards
it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after
13 is eventually called and its middle column is completely marked. If you were
to keep playing until this point, the second board would have a sum of unmarked
numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score
be?
"""
import os
import logging
from typing import List

import day04_0 as old

logging.basicConfig(level=logging.DEBUG)

TEST_PATH = os.path.join(os.path.dirname(__file__), "testing", "day04.txt")



def play_to_lose(numbers: List[int], boards: List[old.Board]) -> int:
    n_won = 0
    while True:
        last_number = numbers.pop(0)
        logging.info(f"Last number: {last_number}")
        boards = old.place_number(last_number, boards)
        n_won = sum(old.has_bingo(board) for board in boards)
        logging.info(f"{n_won} boards have bingo")
        if n_won == len(boards) - 1:
            break
    logging.info("Down to the last board")
    for board in boards:
        logging.info("Scanning...")
        if not old.has_bingo(board):
            logging.info("Found it.")
            break
    while True:
        logging.info("Should be just one more number...")
        last_number = numbers.pop(0)
        logging.info(f"Last number: {last_number}")
        old.place_number(last_number, [board])
        if old.has_bingo(board):
            return old.score_board(board, last_number)


def main():
    test_numbers, test_boards = old.load_data(TEST_PATH)
    test = play_to_lose(test_numbers, test_boards)
    assert test == 1924
    numbers, boards = old.load_data(old.PATH)
    print(play_to_lose(numbers, boards))

if __name__ == "__main__":
    main()
