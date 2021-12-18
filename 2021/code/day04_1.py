"""https://adventofcode.com/2021/day/4"""
import logging
from typing import List

import boilerplate as bp
import day04_0 as old

logging.basicConfig(level=logging.DEBUG)

TEST_PATH = bp.get_test_path()


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
